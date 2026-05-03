import { useState } from "react"
import { Outlet } from "react-router-dom"
import Sidebar from "./Sidebar"

export default function Layout() {
  const [collapsed, setCollapsed] = useState(false)

  const toggleSidebar = () => {
    setCollapsed((prev) => !prev)
  }

  return (
    <div className="flex h-screen">
      <Sidebar collapsed={collapsed} onToggle={toggleSidebar} />

      <main className="flex-1 overflow-y-auto p-4">
        <Outlet />
      </main>
    </div>
  )
}