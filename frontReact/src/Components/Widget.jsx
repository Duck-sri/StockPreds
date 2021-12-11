import React from 'react'

const WidgetRow = ({ id, value }) => {
  return (
    <div className='widget-row'>
      <p style={{ color: 'black' }}>{id}</p>
      <p style={{ color: 'red' }}>{value}</p>
    </div>
  )
}


const Widget = (props) => {
  return (
    <div className={props.title}>
      <h3>{props.title}</h3>
      {
        props.data && Object.entries(props.data).map(ele => <WidgetRow id={ele[0]} value={ele[1]} />)
      }
    </div>
  )
}

export default Widget
