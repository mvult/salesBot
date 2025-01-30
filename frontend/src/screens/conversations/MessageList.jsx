import React from 'react';
import { useMessages } from '@/services/useConversations';
import { format } from 'date-fns';

export const MessageList = ({ conversationId }) => {
  const { data: messages, isLoading, error } = useMessages(conversationId);
  console.log({ messages })

  if (isLoading) {
    return <div className="flex justify-center p-4">Loading messages...</div>;
  }

  if (error) {
    return <div className="text-red-500 p-4">Error loading messages: {error.message}</div>;
  }

  return (
    <div className="flex flex-col space-y-4 p-4">
      {messages?.map((message) => (
        <div
          key={message.id}
          className={`flex flex-col ${message.role === 'assistant'
            ? 'items-start'
            : 'items-end'
            }`}
        >
          <div
            className={`max-w-[80%] rounded-lg p-4 ${message.role === 'assistant'
              ? 'bg-gray-200 text-black'
              : 'bg-blue-500 text-white'
              }`}
          >
            <div className="font-semibold mb-1">
              {message.role === 'assistant' ? '🤖 Assistant' : '👤 User'}
            </div>
            <div className="whitespace-pre-wrap">{message.content}</div>
            <div className="mt-2 text-xs opacity-70">
              <div>
                {format(new Date(message.create_time), 'MMM d, yyyy h:mm a')}
              </div>
              {message.bundle_id && (
                <div className="text-xs">
                  Bundle: {message.bundle_id}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};



