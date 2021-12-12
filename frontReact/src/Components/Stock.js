import React, {useState} from 'react'
import Widget from './Widget'

import data from './data.json'
import  Grid  from '@material-ui/core/Grid';

function Stock(props) {
  const [Symbol, setSymbol] = useState(props.title);

  const renderStock = () => {
    let symbol = document.getElementById('ticker').value;
    // TODO: do api magic
    // data = apiMagic();
    setSymbol(symbol);
  }

  return (
    <div className='stock'>
           <div style={{width:'80%',margin:'5px'}}>
           <label for='ticker' >Ticker : </label>
           <input
              type='text'
              name='ticker'
              required='required'
              id = 'ticker'
              placeholder='ICICIBANK.NS'
              style={{alignSelf:'center',margin:'5px'}}
              >
            </input>
           <button onClick={renderStock}>Get</button>
           </div>
      {props.title && (<h1>{Symbol}</h1>)}
      {/* <Symbol /> */}
      <Grid  margin= '5px 0px 5px'>
          <Grid container
                direction="row"
                justifyContent="flex-start"
                margin= '5px 0px 5px'
               >
               <Grid item> <Widget title='Fundamentals' data={data}/></Grid>
               <Grid item> <Widget title='Financials' data={data}/> </Grid>
          </Grid>
          <Grid > <Widget title='Dividends' data={data}/></Grid>
      </Grid>
      {/* <Chart /> */}
    </div>
  )
}

export default Stock
