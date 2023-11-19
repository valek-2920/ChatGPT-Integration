import { useState } from "react";
import Title from "./Title.js";
import Recorder from "./Recorder.js";
import axios from "axios";

function HomeController() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  const createBlobUrl = (data: any) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    const myMessages = { sender: "me", blobUrl: blobUrl };
    const messagesArr = [...messages, myMessages];

    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        try {
          var response = await axios.post(
            "http://localhost:8000/post-audio",
            formData,
            {
              headers: { "Content-Type": "audio/mpeg" },
              responseType: "arraybuffer",
            }
          );

          const audio = new Audio();
          audio.src = createBlobUrl(response.data);

          const sarahMessage = { sender: "sarah", blobUrl: audio.src };
          messagesArr.push(sarahMessage);
          setMessages(messagesArr);

          setIsLoading(false);
          audio.play();
        } catch (error) {
          console.log("error post-audio", error);
        }
      });
  };

  return (
    <div className="h-screen overflow-y-hidden">
      <Title setMessages={setMessages} />
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        <div className="mt-5 px-5 ">
          {messages.map((audio, index) => {
            return (
              <div
                key={index + audio.sender}
                className={
                  "flex flex-col " +
                  (audio.sender == "sarah" && "flex items-end")
                }
              >
                <div className="mt-4">
                  <p
                    className={
                      audio.sender == "sarah"
                        ? "text-right mr-2 italic text-green-500"
                        : "ml-2 italic text-blue-500"
                    }
                  >
                    {audio.sender}
                  </p>

                  <audio
                    src={audio.blobUrl}
                    className="appearance-none"
                    controls
                  />
                </div>
              </div>
            );
          })}

          {messages.length == 0 && !isLoading && (
            <div className="text-center font-light italic mt-10">
              Send Sarah a message...
            </div>
          )}

          {isLoading && (
            <div className="text-center font-light italic mt-10 animate-pulse">
              Give me a few seconds...
            </div>
          )}
        </div>
        <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <div className=""></div>
            <Recorder handleStop={handleStop} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomeController;
