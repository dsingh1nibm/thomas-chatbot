import streamlit as st
#checking


#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Chat-Bot 🤖")

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#Contact
#with st.sidebar.expander("📬 Contact"):

 #   st.write("**GitHub:**",
#"[yvann-hub/Robby-chatbot](https://github.com/yvann-hub/Robby-chatbot)")

 #   st.write("**Medium:** "
#"[@yvann-hub](https://medium.com/@yvann-hub)")

 #   st.write("**Twitter:** [@yvann_hub](https://twitter.com/yvann_hub)")
  #  st.write("**Mail** : barbot.yvann@gmail.com")
   # st.write("**Created by Yvann**")


#Title
st.markdown(
    """
    <h2 style='text-align: center;'>Hi! i am your data-aware assistant </h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h3 style='text-align:center;'>I use large language models to provide
    context-sensitive interactions. My goal is to help you better understand your data.
    I support TXT, PDF, CSV, Excel, Youtube transcript, Database and WebEx</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")


#Thomas's Pages
#st.subheader("🚀 Thomas's Pages")
#st.write("""
#- **Thomas-Chat**: General Chat on data (PDF, TXT,CSV) with a [vectorstore](https://github.com/facebookresearch/faiss) (index useful parts(max 4) for respond to the user) | works with [ConversationalRetrievalChain](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html)
#- **Thomas-Sheet** (beta): Chat on tabular data (CSV) | for precise information | process the whole file | works with [CSV_Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html) + [PandasAI](https://github.com/gventuri/pandas-ai) for data manipulation and graph creation
#- **Thomas-Youtube**: Summarize YouTube videos with [summarize-chain](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html)
#""")
#st.markdown("---")


#Contributing
#st.markdown("### 🎯 Contributing")
#st.markdown("""
#**Thomas is under regular development.**
#""", unsafe_allow_html=True)





