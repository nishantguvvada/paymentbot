import { Items } from "../../components/Items";
import { ChatInterface } from "../../components/ChatInterface";

export default function Home() {
  return (
    <>
      <div className="flex flex-row justify-center items-center w-full h-full">
        <ChatInterface/>
        <Items/>
      </div>
    </>
  );
}