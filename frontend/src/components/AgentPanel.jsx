import { useState } from "react";

import {
  Bot,
  MessageCircle,
  Send,
  X,
  Sparkles
} from "lucide-react";


function AgentPanel() {

  const [open, setOpen] = useState(false);

  const [input, setInput] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "agent",
      text:
        "Hi. I'm ChainTwin Agent. Ask me about shipments, losses, suppliers, factories or optimization."
    }
  ]);


  function sendMessage() {

    if (!input.trim()) return;


    const question = input;

    setMessages(prev => [
      ...prev,
      {
        role: "user",
        text: question
      }
    ]);

    setInput("");


    setTimeout(() => {

      let response =
        "I can analyze that using the ChainTwin decision engine.";


      const q = question.toLowerCase();


      if (
        q.includes("loss") ||
        q.includes("losing")
      ) {

        response =
          "The largest modeled contributor to this week's ₹4.82L exposure is delayed Material-X supply, followed by Line-3 downtime. I recommend increasing safety stock and advancing the next S-14 delivery.";

      }


      if (
        q.includes("truck") ||
        q.includes("shipment")
      ) {

        response =
          "Shipment CT-2048 is approximately 67% complete. Its primary route intersects the active NH-16 disruption zone, so ChainTwin has generated a lower-risk alternative.";

      }


      if (
        q.includes("next week") ||
        q.includes("optimize")
      ) {

        response =
          "For next week, ChainTwin recommends increasing Material-X safety stock to 1.8 days, moving S-14 delivery six hours earlier, and scheduling Line-3 maintenance on Sunday.";

      }


      setMessages(prev => [
        ...prev,
        {
          role: "agent",
          text: response
        }
      ]);

    }, 500);

  }


  return (
    <>

      <button
        className="agent-launcher"
        onClick={() => setOpen(true)}
      >

        <Sparkles size={18} />

        Ask ChainTwin

      </button>


      {open && (

        <div className="agent-panel">

          <div className="agent-header">

            <div className="agent-title">

              <div className="agent-logo">
                <Bot size={21} />
              </div>

              <div>
                <strong>ChainTwin Agent</strong>

                <span>
                  <i></i>
                  Intelligence online
                </span>
              </div>

            </div>


            <button
              onClick={() => setOpen(false)}
            >
              <X />
            </button>

          </div>


          <div className="suggestions">

            <button
              onClick={() =>
                setInput(
                  "Why are we losing money?"
                )
              }
            >
              Why are we losing money?
            </button>

            <button
              onClick={() =>
                setInput(
                  "Optimize next week"
                )
              }
            >
              Optimize next week
            </button>

            <button
              onClick={() =>
                setInput(
                  "Where is my shipment?"
                )
              }
            >
              Where is CT-2048?
            </button>

          </div>


          <div className="agent-messages">

            {messages.map((message, index) => (

              <div
                key={index}
                className={`message ${message.role}`}
              >

                {message.role === "agent" && (
                  <MessageCircle size={15} />
                )}

                <p>{message.text}</p>

              </div>

            ))}

          </div>


          <div className="agent-input">

            <input
              value={input}
              placeholder="Ask ChainTwin anything..."
              onChange={(e) =>
                setInput(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button onClick={sendMessage}>
              <Send size={17} />
            </button>

          </div>

        </div>

      )}

    </>
  );
}

export default AgentPanel;