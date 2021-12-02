import React, {useState} from 'react'
import Widget from './Widget'

import data from './data.json'

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
        <label for='ticker'>Ticker</label>
        <input
        type='text'
        name='ticker'
        required='required'
        id = 'ticker'
        placeholder='ICICIBANK.NS'>
        </input>
      <button onClick={renderStock}>Get</button>
      {props.title && (<h1>{Symbol}</h1>)}
      {/* <Symbol /> */}
      <Widget title='fundamentals' data={data}/>
      <Widget title='financials' data={data}/>
      <Widget title='dividends' data={data}/>
      {/* <Chart /> */}
    </div>
  )
}

export default Stock
