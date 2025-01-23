import { useAgents } from "@/services/useAgents"
import { AgentItem } from "./AgentItem"

export const AgentList = () => {
  const { data: agents } = useAgents()
  console.log({ agents })

  return (
    <>
      {agents?.map((agent) => <AgentItem key={agent.id} agent={agent} />)}
    </>
  )
}
