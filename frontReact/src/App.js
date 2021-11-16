import React from "react"

import NavBar from './Components/NavBar'
import Stock from './Components/Stock'

const App = () => {
  return (
    <div>
      <NavBar />
      <Stock title='stock_name'/>
    </div>
  )
}

export default App;