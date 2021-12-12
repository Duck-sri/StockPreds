import React from 'react'
import Grid from '@material-ui/core/Grid';
const WidgetRow = ({id,value}) => {
  return (
    <div className='widget-row'>
      <p style={{color : 'black'}}>{id} : {value}</p>
    </div>
  )
}


function Widget(props) { 
  if(props.title==='Fundamentals'){return(
    <Grid>
    <div className={props.title}style={{ height:'400px',width:'630px',border: '2px solid black',borderRadius: '16px',padding:'5px',margin:'10px'}}>
      <h2>{props.title}</h2>
      {
        props.data && Object.entries(props.data).map(ele => <WidgetRow id={ele[0]} value={ele[1]}/>)
      }
    </div>
    </Grid>
  )}
else if(props.title==='Financials'){ return (
  <Grid>
  <div className={props.title}style={{height:'400px', width:'630px',border: '2px solid black',borderRadius: '16px',padding:'5px',margin:'10px'}}>
    <h2>{props.title}</h2>
    {
      props.data && Object.entries(props.data).map(ele => <WidgetRow id={ele[0]} value={ele[1]}/>)
    }
  </div>
  </Grid>
)
   
}
else{return (
  <Grid>
  <div className={props.title}style={{height:'400px', width: '1300px',border: '2px solid black',borderRadius: '16px',padding:'5px',margin:'10px'}}>
    <h2>{props.title}</h2>
    {
      props.data && Object.entries(props.data).map(ele => <WidgetRow id={ele[0]} value={ele[1]}/>)
    }
  </div>
  </Grid>
)

}
}

export default Widget
