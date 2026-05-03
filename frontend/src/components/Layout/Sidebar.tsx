import { NavLink } from "react-router-dom"
import { MessageSquare, Upload, FileText, Menu } from "lucide-react"

type Props = {
  collapsed: boolean
  onToggle: () => void
}

export default function Sidebar({ collapsed, onToggle }: Props) {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-3 py-2 rounded transition ${
      isActive
        ? "bg-blue-500 text-white"
        : "text-gray-700 hover:bg-gray-200"
    }`

  return (
    <div
      className={`border-r p-3 flex flex-col transition-all duration-300 ${
        collapsed ? "w-20" : "w-64"
      }`}
    >
      {/* Top section */}
      <div className="flex items-center justify-between mb-4">
        {!collapsed && (
          <h2 className="text-lg font-bold">RAG App</h2>
        )}

        <button
          onClick={onToggle}
          className="p-2 rounded hover:bg-gray-200"
        >
          <Menu size={18} />
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-2">
        <NavLink to="/" className={linkClass}>
          <MessageSquare size={18} />
          {!collapsed && <span>Chat</span>}
        </NavLink>

        <NavLink to="/upload" className={linkClass}>
          <Upload size={18} />
          {!collapsed && <span>Upload</span>}
        </NavLink>

        <NavLink to="/docs" className={linkClass}>
          <FileText size={18} />
          {!collapsed && <span>Documents</span>}
        </NavLink>
      </nav>
    </div>
  )
}