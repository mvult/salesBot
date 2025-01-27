import { useState } from "react"

import { useAgents } from "@/services/useAgents"
import { AgentItem } from "./AgentItem"
import { AgentDetail } from "./AgentDetail"

export const AgentList = () => {
  const { data: agents } = useAgents()

  const [activeAgentId, setActiveAgentId] = useState(null)
  const [isAdding, setIsAdding] = useState(false)

  const inDetail = activeAgentId || isAdding

  const back = () => {
    setIsAdding(false)
    setActiveAgentId(null)
  }

  return (
    <div className="min-w-full">
      {inDetail && <AgentDetail back={back} agent={agents.find((agent) => agent.id === activeAgentId)} />}

      {!inDetail &&
        <div>
          <button onClick={() => setIsAdding(true)}>
            Add Agent
          </button>
          {agents?.map((agent) => <AgentItem
            key={agent.id}
            agent={agent}
            selectAgent={() => setActiveAgentId(agent.id)}
          />)}
        </div>
      }
    </div>
  )
}
