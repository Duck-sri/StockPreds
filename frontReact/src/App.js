import React from "react"
import NavBar from './Components/NavBar'
import Stock from './Components/Stock'

const App = () => {
  return (
    <div style= {{
    backgroundRepeat: 'no-repeat',
    height: '100%',
    backgroundPosition: 'center',
    backgroundSize: 'cover' }}>
  
    <NavBar />
      <Stock title='Stock Name'/>
    </div>
  )
}

export default App;
