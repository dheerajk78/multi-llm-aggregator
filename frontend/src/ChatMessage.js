export default function ChatMessage({ text, isUser, usage }) {
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
      <div className={`max-w-xs p-3 rounded-lg ${isUser ? "bg-blue-500 text-white" : "bg-gray-200 text-black"}`}>
        <div>{text}</div>
        {usage && !isUser && (
          <div className="text-xs text-gray-500 mt-1">
            Tokens: {usage.total_tokens} (prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})
          </div>
        )}
      </div>
    </div>
  );
}
