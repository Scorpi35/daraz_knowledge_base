import pickle

FAQ = [
    "How do I find refund voucher?",
    "https://helpcenter.daraz.com.np/page/knowledge?pageId=13&category=1000001273&knowledge=1000019621&language=en",
    "How long is the return process?",
    ""
]

with open('Knowledge_Base/Question_Answers/my_account.pkl', 'rb') as f:
    for item in pickle.load(f):
        print(item)

