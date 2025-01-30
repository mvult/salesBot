import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { url_base } from '@/config';

// Fetch conversations from the API
const fetchConversations = async () => {
  console.log("fetching conversations")
  const response = await axios.get(`${url_base}/conversations`);
  return response.data;
};

// React Query hook for fetching conversations
export const useConversations = () => {
  return useQuery({
    queryKey: ['conversations'],
    queryFn: fetchConversations,
    // staleTime: 1000 * 60 * 5, // Data is considered fresh for 5 minutes
    refetchOnWindowFocus: false,
  });
};

const deleteConversation = async (conversationId) => {
  const response = await axios.delete(`${url_base}/conversations/${conversationId}`);
  return response.data;
};

export const useDeleteConversation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteConversation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
    onError: (error) => {
      console.error('Error deleting conversation:', error);
    },
  });
};

const updateConversation = async ({ id, conversationData }) => {
  const response = await axios.patch(`${url_base}/conversations/${id}`, conversationData);
  return response.data;
};

export const useUpdateConversation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateConversation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
    onError: (error) => {
      console.error('Error updating conversation:', error);
    },
  });
};

const fetchMessages = async (conversationId) => {
  const response = await axios.get(`${url_base}/conversations/${conversationId}/messages`);
  return response.data;
};

export const useMessages = (conversationId) => {
  return useQuery({
    queryKey: ['messages', conversationId],
    queryFn: () => fetchMessages(conversationId),
    refetchOnWindowFocus: false,
    enabled: !!conversationId,
  });
};
