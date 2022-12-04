import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = preprocess.preprocess(data)
    
    
    #fetch unique user
    
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox("Show Analysis with respect to ",user_list)
    
    if st.sidebar.button("Show Analysis"):
        
        num_messages,words, num_media_messages, links = helper.fetch_stats(selected_user,df)
        
        st.title('Top Statistics')
        col1,col2,col3,col4 = st.columns(4)
        
        
        with col1:
            st.header("Total messages")
            st.text(num_messages)
            
        with col2:
            st.header("Total Words")
            st.text(words)
            
        with col3:
            st.header("Total Media Shared")
            st.text(num_media_messages)
       
        with col4:
            st.header("Total links Shared")
            st.text(links)
            
        #monthly_timeline
        
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        #daily_timeline
        
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        
        ax.plot(daily_timeline['only_date'],daily_timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        
        if selected_user =='Overall':
            st.title('Most busy users')
            x,new_df = helper.fetch_most_busy_users(df)
            fig,ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color = 'red' )
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


            #wordcloud
            st.title("WordCloud")
            df_wc = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            plt.imshow(df_wc)
            st.pyplot(fig)

            #most common words

            most_common_df = helper.most_common_words(selected_user,df)

            fig,ax = plt.subplots()

            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title('Most commmon words')
            st.pyplot(fig)
            
        # emoji analysis
        
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')
        
        col1,col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)