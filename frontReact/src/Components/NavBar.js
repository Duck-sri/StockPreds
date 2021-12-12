import React from 'react'

function NavBar() {
  return (
    <div className='navbar' style={{float:'right'}}>
      <p className='date'>{new Date().toUTCString()}</p>
    </div>
  )
}

export default NavBar
