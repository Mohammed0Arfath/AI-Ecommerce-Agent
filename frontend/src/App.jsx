import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Loader2, Send, Database, BarChart3, MessageSquare, Sparkles, TrendingUp, ShoppingCart, DollarSign, Eye } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

const API_BASE_URL = 'http://localhost:5000'

function App() {
  const [question, setQuestion] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [streamingText, setStreamingText] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [apiHealth, setApiHealth] = useState(null)
  const [activeTab, setActiveTab] = useState('query')

  // Example questions
  const exampleQuestions = [
    "What is the total sales?",
    "Calculate the RoAS (Return on Ad Spend)",
    "Which product had the highest CPC?",
    "Show me products that are not eligible for advertising",
    "What are the top 10 products by impressions?",
    "Which products have the highest ad spend?"
  ]

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth()
  }, [])

  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`)
      const data = await response.json()
      setApiHealth(data)
    } catch (err) {
      setApiHealth({ status: 'unhealthy', error: 'API not accessible' })
    }
  }

  const handleQuery = async (queryText = question, visualize = false) => {
    if (!queryText.trim()) return

    setIsLoading(true)
    setError(null)
    setResults(null)
    setStreamingText('')

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: queryText,
          visualize: visualize
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleStreamQuery = async (queryText = question) => {
    if (!queryText.trim()) return

    setIsStreaming(true)
    setError(null)
    setResults(null)
    setStreamingText('')

    try {
      const response = await fetch(`${API_BASE_URL}/stream_query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: queryText
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              
              if (data.status === 'typing' && data.char) {
                setStreamingText(prev => prev + data.char)
              } else if (data.status === 'complete') {
                setResults(data)
              } else if (data.status === 'error') {
                setError(data.error)
              }
            } catch (e) {
              // Ignore JSON parsing errors for incomplete chunks
            }
          }
        }
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setIsStreaming(false)
    }
  }

  const formatTableData = (results, columnNames) => {
    if (!results || !columnNames) return null

    return (
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300 rounded-lg">
          <thead>
            <tr className="bg-gray-50">
              {columnNames.map((col, idx) => (
                <th key={idx} className="border border-gray-300 px-4 py-2 text-left font-semibold">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {results.map((row, idx) => (
              <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                {row.map((cell, cellIdx) => (
                  <td key={cellIdx} className="border border-gray-300 px-4 py-2">
                    {cell !== null ? cell.toString() : 'NULL'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl text-white">
              <Sparkles className="w-8 h-8" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Agent for E-commerce Data
            </h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Ask questions about your e-commerce data in natural language. Get instant insights with AI-powered SQL generation and beautiful visualizations.
          </p>
          
          {/* API Health Status */}
          <div className="mt-4 flex justify-center">
            {apiHealth && (
              <Badge variant={apiHealth.status === 'healthy' ? 'default' : 'destructive'} className="px-3 py-1">
                <Database className="w-4 h-4 mr-1" />
                API {apiHealth.status === 'healthy' ? 'Connected' : 'Disconnected'}
                {apiHealth.tables && ` • ${apiHealth.tables.length} tables loaded`}
              </Badge>
            )}
          </div>
        </motion.div>

        {/* Main Interface */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="query" className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4" />
              Query Interface
            </TabsTrigger>
            <TabsTrigger value="examples" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Example Queries
            </TabsTrigger>
          </TabsList>

          <TabsContent value="query" className="space-y-6">
            {/* Query Input */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="w-5 h-5" />
                  Ask Your Question
                </CardTitle>
                <CardDescription>
                  Type your question in natural language about sales, advertising metrics, or product eligibility.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="e.g., What is the total sales for item_id 0? or Which product had the highest CPC?"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  className="min-h-[100px] resize-none"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                      handleQuery()
                    }
                  }}
                />
                <div className="flex gap-2 flex-wrap">
                  <Button 
                    onClick={() => handleQuery(question, false)}
                    disabled={isLoading || isStreaming || !question.trim()}
                    className="flex items-center gap-2"
                  >
                    {isLoading ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Send className="w-4 h-4" />
                    )}
                    Query Data
                  </Button>
                  <Button 
                    onClick={() => handleQuery(question, true)}
                    disabled={isLoading || isStreaming || !question.trim()}
                    variant="outline"
                    className="flex items-center gap-2"
                  >
                    {isLoading ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <BarChart3 className="w-4 h-4" />
                    )}
                    Query + Visualize
                  </Button>
                  <Button 
                    onClick={() => handleStreamQuery(question)}
                    disabled={isLoading || isStreaming || !question.trim()}
                    variant="secondary"
                    className="flex items-center gap-2"
                  >
                    {isStreaming ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Sparkles className="w-4 h-4" />
                    )}
                    Stream Response
                  </Button>
                </div>
                <p className="text-sm text-gray-500">
                  Press Ctrl+Enter to submit • Use "Query + Visualize" for charts
                </p>
              </CardContent>
            </Card>

            {/* Streaming Response */}
            <AnimatePresence>
              {isStreaming && streamingText && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Loader2 className="w-5 h-5 animate-spin" />
                        AI Response (Streaming)
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="bg-gray-50 p-4 rounded-lg font-mono text-sm whitespace-pre-wrap">
                        {streamingText}
                        <span className="animate-pulse">|</span>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Error Display */}
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                >
                  <Alert variant="destructive">
                    <AlertDescription>
                      <strong>Error:</strong> {error}
                    </AlertDescription>
                  </Alert>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Results Display */}
            <AnimatePresence>
              {results && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-6"
                >
                  {/* Query Summary */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Database className="w-5 h-5" />
                        Query Summary
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div>
                        <strong>Question:</strong> {results.question}
                      </div>
                      <div>
                        <strong>Generated SQL:</strong>
                        <pre className="bg-gray-100 p-3 rounded-lg mt-2 text-sm overflow-x-auto">
                          {results.sql_query}
                        </pre>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span className="flex items-center gap-1">
                          <TrendingUp className="w-4 h-4" />
                          {results.row_count} rows returned
                        </span>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Data Visualization */}
                  {results.chart_image_base64 && (
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                          <BarChart3 className="w-5 h-5" />
                          Data Visualization
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="flex justify-center">
                          <img 
                            src={`data:image/png;base64,${results.chart_image_base64}`}
                            alt="Query Results Chart"
                            className="max-w-full h-auto rounded-lg shadow-sm"
                          />
                        </div>
                      </CardContent>
                    </Card>
                  )}

                  {/* Data Table */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Eye className="w-5 h-5" />
                        Raw Data ({results.row_count} rows)
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      {formatTableData(results.results, results.column_names)}
                    </CardContent>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>
          </TabsContent>

          <TabsContent value="examples" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5" />
                  Example Questions
                </CardTitle>
                <CardDescription>
                  Try these sample questions to explore your e-commerce data
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-3">
                  {exampleQuestions.map((q, idx) => (
                    <motion.div
                      key={idx}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Card 
                        className="cursor-pointer hover:shadow-md transition-shadow border-l-4 border-l-blue-500"
                        onClick={() => {
                          setQuestion(q)
                          setActiveTab('query')
                        }}
                      >
                        <CardContent className="p-4">
                          <div className="flex items-center justify-between">
                            <span className="font-medium">{q}</span>
                            <div className="flex gap-2">
                              <Button 
                                size="sm" 
                                variant="outline"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  handleQuery(q, false)
                                }}
                              >
                                Query
                              </Button>
                              <Button 
                                size="sm"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  handleQuery(q, true)
                                }}
                              >
                                Visualize
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Database Schema Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="w-5 h-5" />
                  Available Data Tables
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <ShoppingCart className="w-5 h-5 text-blue-600" />
                      <h3 className="font-semibold text-blue-900">Ad Sales</h3>
                    </div>
                    <p className="text-sm text-blue-700">
                      Advertising metrics including ad sales, impressions, spend, clicks, and units sold
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <DollarSign className="w-5 h-5 text-green-600" />
                      <h3 className="font-semibold text-green-900">Total Sales</h3>
                    </div>
                    <p className="text-sm text-green-700">
                      Overall sales data with total sales amounts and units ordered
                    </p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Eye className="w-5 h-5 text-purple-600" />
                      <h3 className="font-semibold text-purple-900">Eligibility</h3>
                    </div>
                    <p className="text-sm text-purple-700">
                      Product eligibility status for advertising with detailed messages
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

