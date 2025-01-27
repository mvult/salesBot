import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { url_base } from '@/config';

// Fetch agents from the API
const fetchAgents = async () => {
  const response = await axios.get(`${url_base}/agents`); // Replace with your API URL
  return response.data; // Return the data
};

// React Query hook for fetching agents
export const useAgents = () => {
  return useQuery({
    queryKey: ['agents'], // Unique key for this query
    queryFn: fetchAgents, // Function to fetch data
    staleTime: 1000 * 60 * 5, // Data is considered fresh for 5 minutes
    refetchOnWindowFocus: false, // Disable refetching on window focus
  });
};

const deleteAgent = async (agentId) => {
  const response = await axios.delete(`${url_base}/agents/${agentId}`);
  return response.data; // Return the deleted agent data (if needed)
};

export const useDeleteAgent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteAgent, // Function to perform the DELETE request
    onSuccess: () => {
      // Invalidate the "agents" query to refetch the updated list
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
    onError: (error) => {
      console.error('Error deleting agent:', error);
    },
  });
};

const createAgent = async (agentData) => {
  const response = await axios.post(`${url_base}/agents`, agentData);
  return response.data;
};

export const useCreateAgent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createAgent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
    onError: (error) => {
      console.error('Error creating agent:', error);
    },
  });
};


const updateAgent = async ({ id, agentData }) => {
  const response = await axios.patch(`${url_base}/agents/${id}`, agentData);
  return response.data; // Return the updated agent object
};

export const useUpdateAgent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateAgent,
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
    onError: (error) => {
      console.error('Error updating agent:', error);
    },
  });
};
