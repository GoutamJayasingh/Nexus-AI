import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [loaded, setLoaded] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    const savedMessages =
      localStorage.getItem("messages");

    if (savedMessages) {
      setMessages(
        JSON.parse(savedMessages)
      );
    }

  setLoaded(true);
}, []);

  useEffect(() => {
    if (!loaded) return;

    localStorage.setItem(
      "messages",
      JSON.stringify(messages)
    );
  }, [messages, loaded]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const askAgent = async () => {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuestion,
        time: new Date().toLocaleTimeString(),
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const formData = new FormData();

      formData.append(
        "question",
        userQuestion
      );

      if (file) {
        formData.append(
          "file",
          file
        );
      }

      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        formData
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.data.answer,
          tool: res.data.tool,
          time: new Date().toLocaleTimeString(),
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "❌ Error connecting to backend",
          time: new Date().toLocaleTimeString(),
        },
      ]);
    }

    setLoading(false);
  };

  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem("messages");
  };

  return (
    <div className="app">

      {/* Sidebar */}
      <div className="sidebar">

        <div className="logo">
          <h2>🚀 Nexus AI</h2>
          <p>Your Intelligent Workspace</p>
        </div>

        <button
          className="new-chat-btn"
          onClick={clearChat}
        >
          + New Chat
        </button>

        <input
          type="file"
          id="fileUpload"
          hidden
          onChange={(e) => {
            setFile(
              e.target.files[0]
            );
          }}
        />

        <div
          className="menu"
          onClick={() =>
            document
              .getElementById(
                "fileUpload"
              )
              .click()
          }
        >
          📄 Upload File
        </div>

        <div className="menu">
          🕒 Chat History
        </div>

        <div className="menu">
          🌐 Web Search
        </div>

        <div className="menu">
          📊 Excel Analysis
        </div>

        <div className="menu">
          🐍 Python Reader
        </div>

        <div className="menu">
          📑 PDF Reader
        </div>

      </div>

      {/* Main Area */}
      <div className="main-content">

        <div className="welcome">
          <h1>Hello 👋</h1>
          <p>
            Ask questions, analyze files,
            and explore information.
          </p>
        </div>

        <div className="chat-container">

          {messages.length === 0 && (
            <div
              style={{
                textAlign: "center",
                marginTop: "100px",
                color: "#94a3b8",
              }}
            >
              Start a conversation
              with Nexus AI
            </div>
          )}

          {messages.map(
            (msg, index) => (
              <div
                key={index}
                className={`message ${msg.role}`}
              >
                <>
                  <div className="message-time">
                    {msg.time}
                  </div>

                  {msg.tool && (
                    <div className="tool-badge">
                      🛠 {msg.tool.toUpperCase()}
                    </div>
                  )}

                  <ReactMarkdown>
                    {msg.content}
                  </ReactMarkdown>
                </>
              </div>
            )
          )}

          <div ref={bottomRef}></div>

          {loading && (
            <div className="message assistant">
              Thinking...
            </div>
          )}

        </div>

        {/* Input Section */}

        <div className="input-wrapper">

          {file && (
            <div className="file-card">

              <div className="file-left">

                <span className="file-icon">
                  {file.name.endsWith(".pdf") && "📄"}
                  {file.name.endsWith(".xlsx") && "📊"}
                  {file.name.endsWith(".py") && "🐍"}
                </span>

                <span className="file-name">
                  {file.name}
                </span>

              </div>

              <button
                className="remove-file"
                onClick={() => setFile(null)}
              >
                ✕
              </button>

            </div>
          )}

          <div className="input-area">

            <input
              type="text"
              placeholder="Ask anything..."
              value={question}
              onChange={(e) =>
                setQuestion(
                  e.target.value
                )
              }
              onKeyDown={(e) => {
                if (
                  e.key === "Enter"
                ) {
                  askAgent();
                }
              }}
            />

            <button
              onClick={askAgent}
            >
              ➤
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default App;