class Client:
   def __init__(self, name, details, industry, project_requirement):
       self.name = name
       self.details = details
       self.industry = industry
       self.project_requirement = project_requirement

   def __str__(self):
       return f"Client: {self.name}"

   def __repr__(self):
       return f"Client(name='{self.name}', industry='{self.industry}')"

# Example instantiation
zus_coffee = Client(
    name="Zus Coffee",
    details="A coffee chain based in Malaysia, with 500 outlets, handling both offline and online orders. Sells food, beverages and merchandises",
    industry="Food and Beverage in Malaysia looking to expand internationally",
    project_requirement="Develop a chatbot that provides customer service support, including handling common inquiries, order tracking, menu updates, and resolving customer complaints efficiently."
)

ssm= Client(
    name="SSM",
    details="The Companies Commission of Malaysia (SSM), or Suruhanjaya Syarikat Malaysia, is a statutory body established under the Companies Commission of Malaysia Act 2001 to regulate companies and businesses in Malaysia. Its primary functions include registering businesses, enforcing compliance with the Companies Act 2016, maintaining business and company records, and promoting good corporate governance. SSM also provides public access to company information, supports entrepreneurship through streamlined processes like EzBiz, and fosters ethical business practices. It plays a vital role in ensuring transparency, accountability, and lawful operation of businesses in Malaysia.",
    industry="business and corporate governance sector",
    project_requirement="""The project aims to develop an AI-powered conversational chatbot for the Companies Commission of Malaysia (SSM) to provide accurate and user-friendly support to business owners and prospective entrepreneurs. The chatbot will assist with common queries, such as using the MBRS system, by leveraging a Retrieval-Augmented Generation (RAG) framework to access a comprehensive knowledgebase built from SSM’s existing documentation. This ensures accurate, reliable responses while minimizing hallucinations. Additionally, the system will include an automated data ingestion pipeline to update the knowledgebase whenever documentation changes, ensuring the chatbot remains up-to-date.
The solution is designed to reduce dependency on human agents by handling repetitive queries, allowing them to focus on more complex issues. It will also be scalable to support nationwide traffic, ensuring accessibility for users of varying technical expertise. This project will enhance customer satisfaction, improve operational efficiency, and future-proof SSM's customer engagement systems with a modern, scalable, and automated platform"""
)

game= Client(
    name="PB Gaming",
    details="The client is a licensed online gaming platform that provides a diverse range of gaming experiences to users worldwide. Their focus is on delivering seamless, engaging, and secure gaming experiences, supported by innovative technologies and exceptional customer service. By integrating advanced solutions, the platform aims to enhance user satisfaction, build loyalty, and maintain operational efficiency while ensuring compliance with industry regulations.",
    industry="online gaming and entertainment sector",
    project_requirement= """The project aims to develop an AI-powered conversational chatbot to act as a humanized customer service agent, enhancing the customer experience while maintaining a lean support team. The chatbot will handle common customer inquiries, such as account issues, game instructions, and troubleshooting, ensuring accurate and consistent responses. If the chatbot is unable to resolve a customer’s issue, it will integrate seamlessly with LiveChat.com for a smooth user agent handover, ensuring uninterrupted support.
    The solution focuses on reducing the need for human agents by automating repetitive tasks, delivering a personalized and consistent experience to users. It will be designed to provide efficient support at scale, meeting the high-demand environment of online gaming. This phase of development will prioritize backend integration with LiveChat.com, enabling real-time escalation for complex issues while ensuring the chatbot serves as a reliable, round-the-clock first point of contact. The project aims to improve operational efficiency, reduce costs, and provide a unified, high-quality support experience for users"""
)