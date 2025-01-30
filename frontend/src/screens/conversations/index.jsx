import { useState } from 'react';
import { useConversations } from '@/services/useConversations';
import ConversationItem from './ConversationItem';
import ConversationDetail from './ConversationDetail';

export const ConversationList = () => {
  const { data: conversations, isLoading, error } = useConversations();
  const [selectedConvoId, setSelectedConvoId] = useState(null);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <p className="text-red-600">Error loading conversations: {error.message}</p>
      </div>
    );
  }

  if (selectedConvoId) {
    return (
      <ConversationDetail
        conversation={conversations.find((c) => c.id === selectedConvoId)}
        onBack={() => setSelectedConvoId(null)}
      />
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Conversations</h1>
      <div className="space-y-4">
        {conversations?.map((conversation) => (
          <ConversationItem
            key={conversation.id}
            conversation={conversation}
            onClick={() => setSelectedConvoId(conversation.id)}
          />
        ))}
      </div>
    </div>
  );
};

