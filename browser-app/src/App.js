import React from 'react';
import './App.css';
import { Table, Collapse, Icon, Divider, Badge, Menu, Dropdown} from 'antd';
import fetchGraphQL from './fetchGraphQL';
import graphql from 'babel-plugin-relay/macro'
import {
  RelayEnvironmentProvider,
  preloadQuery,
  usePreloadedQuery
} from 'react-relay/hooks'
import RelayEnvironment from './RelayEnvironment';
import {Router, Link} from '@reach/router'

const {Suspense} = React

const AllLogsQuery = graphql`
  query AppAllLogsQuery($num: Int!) {
    allLogs(first: $num) {
      edges {
        node {
          id
          hasHourly
          hasDaily
          hasMonthly
          dateCollected
          instrument {
            instrument
          }
        }
      }
    }
    allInstruments(first: $num) {
      edges {
        node {
          id
          instrument
          logs {
            edges {
              node {
                id
                dateCollected
                hasHourly
                hasDaily
                hasMonthly
              }
            }
          }
        }
      }
    }
  }
`;


const preloadedQuery = preloadQuery(RelayEnvironment, AllLogsQuery, {
  "num": 5000/*query vars*/
})

function App(props) {
  const data = usePreloadedQuery(AllLogsQuery, props.preloadedQuery)
  console.log(data)
  return (
    <div className="App">
      <nav>
        <Link to="/">Home</Link>
      </nav>
      <Router>
        <NestedTable path="/" data={data.allInstruments.edges} />
        <Test path ="/test"/>
      </Router>
    </div>
  );
}

function Test(props) {
  return (
  <div>
    <h2>{JSON.stringify(props.location.state.record)}</h2>
  </div>
  )
}

function AppRoot(props){
  return (
    <RelayEnvironmentProvider environment={RelayEnvironment}>
      <Suspense fallback={'Loading...'}>
        <App preloadedQuery={preloadedQuery} />
      </Suspense>
    </RelayEnvironmentProvider>
  );
}

export default AppRoot;

const columns_by_inst = [
  {
    title: 'Instrument',
    dataIndex: 'node.instrument',
    key: 'instrument',
    render: (text, record) => (
    <Link to="/test" state={{record: record.node.instrument}}>{record.node.instrument}</Link>
    )
  },
  {
    title: 'Latest Download Date',
    dataIndex: 'node.dateCollected',
    key: 'dateCollected',
    render: (text, record) => (
      <span>
        {maxDate(record.node.logs.edges)}
      </span>)
  },
]
const maxDate = (all_dates) => {
  var max_dt = all_dates[0].node.dateCollected,
  max_dtObj = new Date(all_dates[0].node.dateCollected);
  all_dates.forEach(function(dt, index){
    if ( new Date( dt.node.dateCollected ) > max_dtObj){
      max_dt = dt.node.dateCollected;
      max_dtObj = new Date(dt.node.dateCollected);
    }
  });
  return max_dtObj.toLocaleDateString({year:'long', month:'numeric', day:'numeric'});
}

function NestedTable(props) {
  const expandedRowRender = (record) => {
    const columns = [
      {
        title: 'Date Collected',
        key: 'dateCollected',
        render: (text, record) => (
          new Date(record.node.dateCollected).toLocaleDateString()
        )
      },
      {
        title: 'Hourly',
        key: 'hourly',
        render: (text, record) => (
          <Link to="/test" state={{record: record}}>
          <span>
            <Icon type={record.node.hasHourly ? "check-circle": "close-circle"} theme="twoTone" twoToneColor="#52c41a"/>
          </span></Link>)
      },
      {
        title: 'Daily',
        key: 'daily',
        render: (text, record) => (
          <span>
            <Icon type={record.node.hasDaily ? "check-circle": "close-circle"} theme="twoTone" twoToneColor="#52c41a"/>
          </span>)
      },
      {
        title: 'Monthly',
        key: 'monthly',
        render: (text, record) => (
          <span>
            <Icon type={record.node.hasMonthly ? "check-circle": "close-circle"} theme="twoTone" twoToneColor="#52c41a"/>
          </span>)
      },

    ];

    const data = record.node.logs.edges
    return <Table columns={columns} dataSource={data} rowKey={(record) => record.node.id} pagination={false} />;
  };

  const data = props.data;
  console.log("data")
  console.log(data)
  return (
    <Table
      className="components-table-demo-nested"
      columns={columns_by_inst}
      expandedRowRender={expandedRowRender}
      dataSource={data}
      rowKey={(record) => record.node.id}
    />
  );
}
