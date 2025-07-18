'use client';

import { useState, useRef, useEffect } from 'react';
import { Plus, MessageSquare, Menu, X, Clock, Scale, Send, User, Bot, LogOut, ChevronDown, ChevronUp, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';

// Mock user data - in a real app, this would come from authentication
const mockUser = {
  id: '1',
  name: 'John Smith',
  email: 'john.smith@example.com',
  avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face&auto=format',
  initials: 'JS'
};

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  userAvatar?: string;
  userInitials?: string;
}

interface ChatSession {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: Date;
  messageCount: number;
  messages: Message[];
}

export default function JurisAIApp() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeSession, setActiveSession] = useState<string>('1');
  const [currentMessage, setCurrentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [documents, setDocuments] = useState<string[]>([]);
  const [recentSessionsMinimized, setRecentSessionsMinimized] = useState(false);

  const [authenticatedUser, setAuthenticatedUser] = useState(mockUser);

  // Load chat sessions from local storage on initial mount
  useEffect(() => {
    const storedSessions = localStorage.getItem('chatSessions');
    if (storedSessions) {
      const parsedSessions = JSON.parse(storedSessions);
      // Re-hydrate dates
      parsedSessions.forEach((session: ChatSession) => {
        session.timestamp = new Date(session.timestamp);
        session.messages.forEach(message => {
          message.timestamp = new Date(message.timestamp);
        });
      });
      setChatSessions(parsedSessions);
      const storedActiveSession = localStorage.getItem('activeSession');
      if (storedActiveSession) {
        setActiveSession(storedActiveSession);
      } else if (parsedSessions.length > 0) {
        setActiveSession(parsedSessions[0].id);
      }
    }
  }, []);

  // Save chat sessions to local storage whenever they change
  useEffect(() => {
    localStorage.setItem('chatSessions', JSON.stringify(chatSessions));
    localStorage.setItem('activeSession', activeSession);
  }, [chatSessions, activeSession]);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      localStorage.setItem('access_token', token);
      window.history.replaceState({}, document.title, "/"); // Clean the URL
    }

    const storedToken = localStorage.getItem('access_token');
    if (!storedToken) {
      window.location.href = '/landing';
      return;
    }

    try {
      const decodedToken = JSON.parse(atob(storedToken.split('.')[1]));
      setAuthenticatedUser({
        ...mockUser,
        name: decodedToken.name || mockUser.name,
        email: decodedToken.sub || mockUser.email,
        avatar: decodedToken.picture || mockUser.avatar,
        initials: decodedToken.name ? decodedToken.name.charAt(0).toUpperCase() : mockUser.initials,
      });
    } catch (error) {
      console.error("Error decoding token:", error);
      localStorage.removeItem('access_token');
      window.location.href = '/landing';
      return;
    }

    const fetchDocuments = async () => {
      try {
        const res = await fetch('http://localhost:8000/documents', {
          headers: {
            'Authorization': `Bearer ${storedToken}`,
          },
        });
        if (!res.ok) {
          throw new Error('Failed to fetch documents.');
        }
        const data = await res.json();
        const apiDocuments = data.documents || [];
        setDocuments(apiDocuments); // Update the documents state

        setChatSessions(prevSessions => {
          const updatedSessionsMap = new Map<string, ChatSession>();

          // 1. Populate map with existing sessions from localStorage (including their messages)
          prevSessions.forEach(session => {
            updatedSessionsMap.set(session.id, session);
          });

          // 2. Process documents from API
          apiDocuments.forEach((doc: string) => {
            const docId = `doc-${doc}`;
            const existingSession = updatedSessionsMap.get(docId);

            if (existingSession) {
              // If session exists, update its title (if necessary) but keep its messages
              updatedSessionsMap.set(docId, {
                ...existingSession,
                title: doc, // Ensure title is up-to-date
              });
            } else {
              // If session doesn't exist, create a new one with empty messages
              updatedSessionsMap.set(docId, {
                id: docId,
                title: doc,
                lastMessage: 'Ask a question about this document',
                timestamp: new Date(),
                messageCount: 0,
                messages: [], // New session, so messages are empty
              });
            }
          });

          // Filter out sessions that are no longer present in apiDocuments
          // This handles cases where documents might have been deleted from the backend
          const currentApiDocIds = new Set(apiDocuments.map((doc: string) => `doc-${doc}`));
          const finalSessions = Array.from(updatedSessionsMap.values()).filter(session =>
            session.id.startsWith('new-session-') || currentApiDocIds.has(session.id)
          );

          return finalSessions;
        });

        // Set active session if none is active and there are sessions
        if (!activeSession && apiDocuments.length > 0) {
          setActiveSession(`doc-${apiDocuments[0]}`);
        }

      } catch (err) {
        console.error('Failed to fetch documents.', err);
        localStorage.removeItem('access_token');
        window.location.href = '/landing';
      }
    };
    fetchDocuments();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatSessions, activeSession]);

  const getCurrentSession = () => {
    return chatSessions.find(session => session.id === activeSession);
  };

  const sendMessage = async () => {
    if (!currentMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: currentMessage.trim(),
      sender: 'user',
      timestamp: new Date(),
      userAvatar: mockUser.avatar,
      userInitials: mockUser.initials
    };

    const currentSession = getCurrentSession();
    const policy_filename = currentSession ? currentSession.title : '';

    if (currentSession && currentSession.messages.length === 0) {
      setChatSessions(prev => prev.map(session => 
        session.id === activeSession 
          ? { 
              ...session, 
              title: policy_filename
            }
          : session
      ));
    }

    // Add user message to current session
    setChatSessions(prev => prev.map(session => 
      session.id === activeSession 
        ? { 
            ...session, 
            messages: [...session.messages, userMessage],
            lastMessage: userMessage.content,
            timestamp: new Date(),
            messageCount: session.messageCount + 1
          }
        : session
    ));

    setCurrentMessage('');
    setIsLoading(true);

    try {
      const storedToken = localStorage.getItem('access_token');
      if (!storedToken) {
        throw new Error('No access token found.');
      }

      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${storedToken}`,
        },
        body: JSON.stringify({
          policy_filename,
          user_query: userMessage.content,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from the backend.');
      }

      const data = await response.json();
      
      let formattedContent = "";
      if (data.decision) {
        formattedContent += `Decision: ${data.decision}\n`;
      }
      if (data.amount !== null) {
        formattedContent += `Amount: ${data.amount}\n`;
      }
      if (data.justification && data.justification.length > 0) {
        formattedContent += "\nJustification:\n";
        data.justification.forEach((item: any, index: number) => {
          formattedContent += `  ${index + 1}. Clause: ${item.clause}\n`;
          formattedContent += `     Reason: ${item.reason}\n`;
        });
      } else if (data.error) {
        formattedContent = `Error: ${data.error}\n`;
        if (data.raw_output) {
          formattedContent += `Raw Output: ${data.raw_output}\n`;
        }
      } else {
        formattedContent = JSON.stringify(data, null, 2); // Fallback for unexpected structure
      }

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: formattedContent,
        sender: 'bot',
        timestamp: new Date()
      };

      // Add bot response to current session
      setChatSessions(prev => prev.map(session => 
        session.id === activeSession 
          ? { 
              ...session, 
              messages: [...session.messages, botMessage],
              lastMessage: botMessage.content,
              timestamp: new Date(),
              messageCount: session.messageCount + 1
            }
          : session
      ));

    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'I apologize, but I encountered an issue processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      };
      setChatSessions(prev => prev.map(session => 
        session.id === activeSession 
          ? { 
              ...session, 
              messages: [...session.messages, errorMessage],
              lastMessage: errorMessage.content,
              timestamp: new Date(),
              messageCount: session.messageCount + 1
            }
          : session
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const createNewSession = () => {
    const newSessionId = `new-session-${Date.now()}`;
    const newSession: ChatSession = {
      id: newSessionId,
      title: 'New Query Session',
      lastMessage: '',
      timestamp: new Date(),
      messageCount: 0,
      messages: []
    };

    setChatSessions(prev => [newSession, ...prev]);
    setActiveSession(newSessionId);
    // Optionally trigger file upload immediately for new sessions
    document.getElementById('file-upload-input')?.click();
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const storedToken = localStorage.getItem('access_token');
      if (!storedToken) {
        throw new Error('No access token found.');
      }

      const response = await fetch('http://localhost:8000/upload_document', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${storedToken}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to upload document.');
      }

      const data = await response.json();
      alert(data.message);

      // Refresh document list
      const res = await fetch('http://localhost:8000/documents', {
        headers: {
          'Authorization': `Bearer ${storedToken}`,
        },
      });
      const updatedData = await res.json();
      setDocuments(updatedData.documents || []);
      const sessions = (updatedData.documents || []).map((doc: string, index: number) => ({
        id: `doc-${doc}`,
        title: doc,
        lastMessage: 'Ask a question about this document',
        timestamp: new Date(),
        messageCount: 0,
        messages: [],
      }));
      // Merge with existing sessions to preserve chat history for non-deleted docs
      setChatSessions(prev => {
        const newDocsMap = new Map(sessions.map(s => [s.title, s]));
        return prev.filter(s => newDocsMap.has(s.title) || s.id.startsWith('new-session-')).map(s => newDocsMap.get(s.title) || s);
      });

    } catch (error: any) {
      alert(`Upload failed: ${error.message}`);
      console.error('Upload error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteDocument = async (filename: string) => {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) {
      return;
    }

    setIsLoading(true);
    try {
      const storedToken = localStorage.getItem('access_token');
      if (!storedToken) {
        throw new Error('No access token found.');
      }

      const response = await fetch(`http://localhost:8000/documents/${filename}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${storedToken}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete document.');
      }

      alert(`Document ${filename} deleted successfully.`);

      // Remove the deleted session from chatSessions
      setChatSessions(prev => prev.filter(session => session.title !== filename));
      // If the active session was deleted, switch to the first available session or default
      if (activeSession === `doc-${filename}`) {
        setActiveSession(chatSessions[0]?.id || '1');
      }

      // Refresh document list (already implemented, but ensure it's correct)
      const res = await fetch('http://localhost:8000/documents', {
        headers: {
          'Authorization': `Bearer ${storedToken}`,
        },
      });
      const updatedData = await res.json();
      setDocuments(updatedData.documents || []);
      const sessions = (updatedData.documents || []).map((doc: string, index: number) => ({
        id: `doc-${doc}`,
        title: doc,
        lastMessage: 'Ask a question about this document',
        timestamp: new Date(),
        messageCount: 0,
        messages: [],
      }));
      // Merge with existing sessions to preserve chat history for non-deleted docs
      setChatSessions(prev => {
        const newDocsMap = new Map(sessions.map(s => [s.title, s]));
        return prev.filter(s => newDocsMap.has(s.title) || s.id.startsWith('new-session-')).map(s => newDocsMap.get(s.title) || s);
      });

    } catch (error: any) {
      alert(`Deletion failed: ${error.message}`);
      console.error('Deletion error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTimestamp = (date: Date) => {
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) {
      const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
      return `${diffInMinutes}m ago`;
    } else if (diffInHours < 24) {
      return `${diffInHours}h ago`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays}d ago`;
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatMessageTime = (date: Date) => {
    return date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const handleSignOut = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/landing';
  };

  const currentSession = getCurrentSession();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 flex">
      {/* Sidebar */}
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-80 bg-white border-r border-gray-200 shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-700 rounded-lg flex items-center justify-center">
                <Scale className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-900">Intelligent Query System</h2>
                <p className="text-xs text-gray-500">LLM-Powered</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>

          {/* New Chat Button */}
          <div className="p-4 border-b border-gray-100">
            <input
              type="file"
              id="file-upload-input"
              style={{ display: 'none' }}
              onChange={handleFileUpload}
              accept=".pdf,.docx,.txt"
            />
            <Button 
              onClick={createNewSession}
              className="w-full bg-blue-700 hover:bg-blue-800 text-white"
              disabled={isLoading}
            >
              <Plus className="w-4 h-4 mr-2" />
              Upload New Document
            </Button>
          </div>

          {/* Chat Sessions */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                  Available Documents
                </h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setRecentSessionsMinimized(!recentSessionsMinimized)}
                  className="h-auto p-1"
                >
                  {recentSessionsMinimized ? (
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  ) : (
                    <ChevronUp className="w-4 h-4 text-gray-500" />
                  )}
                </Button>
              </div>
              {!recentSessionsMinimized && (
                <div className="space-y-2">
                  {chatSessions.map((session) => (
                    <div
                      key={session.id}
                      onClick={() => setActiveSession(session.id)}
                      className={cn(
                        "p-3 rounded-lg cursor-pointer transition-all duration-200 hover:bg-gray-50 border",
                        activeSession === session.id 
                          ? "bg-blue-50 border-blue-200" 
                          : "bg-white border-gray-100 hover:border-gray-200"
                      )}
                    >
                      <div className="flex items-start space-x-3">
                        <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                          <MessageSquare className="w-4 h-4 text-gray-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="text-sm font-medium text-gray-900 truncate">
                            {session.title}
                          </h4>
                          <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                            {session.lastMessage || 'No messages yet'}
                          </p>
                          <div className="flex items-center justify-between mt-2">
                            <div className="flex items-center space-x-1 text-xs text-gray-400">
                              <Clock className="w-3 h-3" />
                              <span>{formatTimestamp(session.timestamp)}</span>
                            </div>
                            <Badge variant="secondary" className="text-xs">
                              {session.messageCount} msgs
                            </Badge>
                          </div>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation(); // Prevent activating the session
                            handleDeleteDocument(session.title);
                          }}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar Footer */}
          <div className="p-4 border-t border-gray-200">
            <Button 
              onClick={handleSignOut}
              className="w-full bg-red-600 hover:bg-red-700 text-white"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Sign Out
            </Button>
            <div className="text-xs text-gray-500 text-center mt-2">
              <p>Intelligent Query System v1.0</p>
              <p className="mt-1">LLM-Powered</p>
            </div>
          </div>
        </div>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Bar */}
        <div className="bg-white border-b border-gray-200 px-4 py-3 lg:px-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden"
              >
                <Menu className="w-5 h-5" />
              </Button>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">
                  {currentSession?.title || 'Intelligent Query System'}
                </h1>
                <p className="text-sm text-gray-500">
                  LLM-Powered Document Analysis
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Badge variant="outline" className="hidden sm:flex">
                {currentSession?.messageCount || 0} messages
              </Badge>
              {/* User Avatar */}
              <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-medium">
                {authenticatedUser.avatar ? (
                  <img 
                    src={authenticatedUser.avatar} 
                    alt="User"
                    className="w-8 h-8 rounded-full object-cover"
                  />
                ) : (
                  authenticatedUser.initials
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col min-h-0">
          {/* Messages */}
          <ScrollArea className="flex-1 p-4 lg:p-6">
            <div className="max-w-4xl mx-auto space-y-4">
              {currentSession?.messages.length === 0 ? (
                <div className="text-center py-12">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Scale className="w-8 h-8 text-blue-600" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Welcome to the Intelligent Query System
                  </h3>
                  <p className="text-gray-600 max-w-md mx-auto">
                    Select a document from the left sidebar and ask a question to get a structured JSON response.
                  </p>
                </div>
              ) : (
                currentSession?.messages.map((message) => (
                  <div
                    key={message.id}
                    className={cn(
                      "flex gap-3 max-w-3xl",
                      message.sender === 'user' ? "ml-auto flex-row-reverse" : "mr-auto"
                    )}
                  >
                    <div className={cn(
                      "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
                      message.sender === 'user' 
                        ? "bg-blue-600 text-white overflow-hidden" 
                        : "bg-gray-100 text-gray-600"
                    )}>
                      {message.sender === 'user' ? (
                        message.userAvatar ? (
                          <img 
                            src={message.userAvatar} 
                            alt="User"
                            className="w-8 h-8 rounded-full object-cover"
                          />
                        ) : (
                          <span className="text-xs font-medium">
                            {message.userInitials || 'U'}
                          </span>
                        )
                      ) : (
                        <Bot className="w-4 h-4" />
                      )}
                    </div>
                    <div className={cn(
                      "flex-1 px-4 py-3 rounded-lg",
                      message.sender === 'user'
                        ? "bg-blue-600 text-white"
                        : "bg-white border border-gray-200"
                    )}>
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">
                        {message.content}
                      </p>
                      <p className={cn(
                        "text-xs mt-2",
                        message.sender === 'user' 
                          ? "text-blue-100" 
                          : "text-gray-500"
                      )}>
                        {formatMessageTime(message.timestamp)}
                      </p>
                    </div>
                  </div>
                ))
              )}
              
              {isLoading && (
                <div className="flex gap-3 max-w-3xl mr-auto">
                  <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0 overflow-hidden">
                    <Bot className="w-4 h-4 text-gray-600" />
                  </div>
                  <div className="flex-1 px-4 py-3 rounded-lg bg-white border border-gray-200">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* Message Input */}
          <div className="border-t border-gray-200 p-4 lg:p-6 bg-white">
            <div className="max-w-4xl mx-auto">
              <div className="flex gap-2">
                <Input
                  placeholder='e.g., "46M, knee surgery, Pune, 3-month policy" or "Is knee surgery covered?"'
                  value={currentMessage}
                  onChange={(e) => setCurrentMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  disabled={isLoading}
                  className="flex-1 h-12 text-base border-gray-200 focus:border-blue-600 focus:ring-blue-600"
                />
                <Button 
                  onClick={sendMessage}
                  disabled={!currentMessage.trim() || isLoading}
                  className="h-12 px-6 bg-blue-700 hover:bg-blue-800 text-white shadow-md hover:shadow-lg transition-all duration-200"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
              <p className="text-xs text-gray-500 mt-2 text-center">
                Press Enter to send • Shift+Enter for new line
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}