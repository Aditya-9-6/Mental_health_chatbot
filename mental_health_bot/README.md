# Mental Health Companion

This is a Streamlit application that provides a safe and supportive space for users to take care of their mental well-being.

## Features

*   **Chat with a supportive AI:** Have a conversation with a mental health assistant that can provide information and support.
*   **Journaling:** Write down your thoughts and feelings in a private journal.
*   **Mood Tracking:** Track your mood over time and visualize it in a graph.
*   **Goal Setting:** Set and track your mental health goals.
*   **Personalized Recommendations:** Get personalized recommendations based on your mood and journal entries.
*   **User Authentication:** Your data is protected with user authentication.

## How to run locally

1.  **Clone the repository:**
    ```bash
    git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set the `GOOGLE_API_KEY` environment variable:**
    Create a `.env` file in the root of the project and add the following line:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY"
    ```
4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
