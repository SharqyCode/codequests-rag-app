import { Routes, Route, Navigate } from "react-router-dom"
import ChatPage from "./pages/ChatPage"
import UploadPage from "./pages/UploadPage"
import DocsPage from "./pages/DocsPage"
import Layout from "./components/Layout/Layout"

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<ChatPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/docs" element={<DocsPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}