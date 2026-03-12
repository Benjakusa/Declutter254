import { useState, useEffect } from "react"

function SearchBar({ onSearch }) {

  const [query, setQuery] = useState("")
  const [debouncedQuery, setDebouncedQuery] = useState("")

  useEffect(() => {

    const timer = setTimeout(() => {
      setDebouncedQuery(query)
    }, 500)

    return () => clearTimeout(timer)

  }, [query])

  useEffect(() => {

    onSearch(debouncedQuery)

  }, [debouncedQuery, onSearch])


  return (

    <div>

      <input
        type="text"
        placeholder="Search items..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

    </div>

  )

}

export default SearchBar 