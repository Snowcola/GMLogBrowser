/**
 * @flow
 * @relayHash 3f81e2a639fc6722cba3836c75c802f4
 */

/* eslint-disable */

'use strict';

/*::
import type { ConcreteRequest } from 'relay-runtime';
export type AppAllLogsQueryVariables = {|
  num: number
|};
export type AppAllLogsQueryResponse = {|
  +allLogs: ?{|
    +edges: $ReadOnlyArray<?{|
      +node: ?{|
        +id: string,
        +hasHourly: ?boolean,
        +hasDaily: ?boolean,
        +hasMonthly: ?boolean,
        +dateCollected: ?any,
        +instrument: ?{|
          +instrument: ?string
        |},
      |}
    |}>
  |},
  +allInstruments: ?{|
    +edges: $ReadOnlyArray<?{|
      +node: ?{|
        +id: string,
        +instrument: ?string,
        +logs: ?{|
          +edges: $ReadOnlyArray<?{|
            +node: ?{|
              +id: string,
              +dateCollected: ?any,
              +hasHourly: ?boolean,
              +hasDaily: ?boolean,
              +hasMonthly: ?boolean,
            |}
          |}>
        |},
      |}
    |}>
  |},
|};
export type AppAllLogsQuery = {|
  variables: AppAllLogsQueryVariables,
  response: AppAllLogsQueryResponse,
|};
*/


/*
query AppAllLogsQuery(
  $num: Int!
) {
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
          id
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
*/

const node/*: ConcreteRequest*/ = (function(){
var v0 = [
  {
    "kind": "LocalArgument",
    "name": "num",
    "type": "Int!",
    "defaultValue": null
  }
],
v1 = [
  {
    "kind": "Variable",
    "name": "first",
    "variableName": "num"
  }
],
v2 = {
  "kind": "ScalarField",
  "alias": null,
  "name": "id",
  "args": null,
  "storageKey": null
},
v3 = {
  "kind": "ScalarField",
  "alias": null,
  "name": "hasHourly",
  "args": null,
  "storageKey": null
},
v4 = {
  "kind": "ScalarField",
  "alias": null,
  "name": "hasDaily",
  "args": null,
  "storageKey": null
},
v5 = {
  "kind": "ScalarField",
  "alias": null,
  "name": "hasMonthly",
  "args": null,
  "storageKey": null
},
v6 = {
  "kind": "ScalarField",
  "alias": null,
  "name": "dateCollected",
  "args": null,
  "storageKey": null
},
v7 = {
  "kind": "ScalarField",
  "alias": null,
  "name": "instrument",
  "args": null,
  "storageKey": null
},
v8 = {
  "kind": "LinkedField",
  "alias": null,
  "name": "allInstruments",
  "storageKey": null,
  "args": (v1/*: any*/),
  "concreteType": "InstrumentConnection",
  "plural": false,
  "selections": [
    {
      "kind": "LinkedField",
      "alias": null,
      "name": "edges",
      "storageKey": null,
      "args": null,
      "concreteType": "InstrumentEdge",
      "plural": true,
      "selections": [
        {
          "kind": "LinkedField",
          "alias": null,
          "name": "node",
          "storageKey": null,
          "args": null,
          "concreteType": "Instrument",
          "plural": false,
          "selections": [
            (v2/*: any*/),
            (v7/*: any*/),
            {
              "kind": "LinkedField",
              "alias": null,
              "name": "logs",
              "storageKey": null,
              "args": null,
              "concreteType": "LogConnection",
              "plural": false,
              "selections": [
                {
                  "kind": "LinkedField",
                  "alias": null,
                  "name": "edges",
                  "storageKey": null,
                  "args": null,
                  "concreteType": "LogEdge",
                  "plural": true,
                  "selections": [
                    {
                      "kind": "LinkedField",
                      "alias": null,
                      "name": "node",
                      "storageKey": null,
                      "args": null,
                      "concreteType": "Log",
                      "plural": false,
                      "selections": [
                        (v2/*: any*/),
                        (v6/*: any*/),
                        (v3/*: any*/),
                        (v4/*: any*/),
                        (v5/*: any*/)
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
};
return {
  "kind": "Request",
  "fragment": {
    "kind": "Fragment",
    "name": "AppAllLogsQuery",
    "type": "Query",
    "metadata": null,
    "argumentDefinitions": (v0/*: any*/),
    "selections": [
      {
        "kind": "LinkedField",
        "alias": null,
        "name": "allLogs",
        "storageKey": null,
        "args": (v1/*: any*/),
        "concreteType": "LogConnectionsConnection",
        "plural": false,
        "selections": [
          {
            "kind": "LinkedField",
            "alias": null,
            "name": "edges",
            "storageKey": null,
            "args": null,
            "concreteType": "LogConnectionsEdge",
            "plural": true,
            "selections": [
              {
                "kind": "LinkedField",
                "alias": null,
                "name": "node",
                "storageKey": null,
                "args": null,
                "concreteType": "Log",
                "plural": false,
                "selections": [
                  (v2/*: any*/),
                  (v3/*: any*/),
                  (v4/*: any*/),
                  (v5/*: any*/),
                  (v6/*: any*/),
                  {
                    "kind": "LinkedField",
                    "alias": null,
                    "name": "instrument",
                    "storageKey": null,
                    "args": null,
                    "concreteType": "Instrument",
                    "plural": false,
                    "selections": [
                      (v7/*: any*/)
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      (v8/*: any*/)
    ]
  },
  "operation": {
    "kind": "Operation",
    "name": "AppAllLogsQuery",
    "argumentDefinitions": (v0/*: any*/),
    "selections": [
      {
        "kind": "LinkedField",
        "alias": null,
        "name": "allLogs",
        "storageKey": null,
        "args": (v1/*: any*/),
        "concreteType": "LogConnectionsConnection",
        "plural": false,
        "selections": [
          {
            "kind": "LinkedField",
            "alias": null,
            "name": "edges",
            "storageKey": null,
            "args": null,
            "concreteType": "LogConnectionsEdge",
            "plural": true,
            "selections": [
              {
                "kind": "LinkedField",
                "alias": null,
                "name": "node",
                "storageKey": null,
                "args": null,
                "concreteType": "Log",
                "plural": false,
                "selections": [
                  (v2/*: any*/),
                  (v3/*: any*/),
                  (v4/*: any*/),
                  (v5/*: any*/),
                  (v6/*: any*/),
                  {
                    "kind": "LinkedField",
                    "alias": null,
                    "name": "instrument",
                    "storageKey": null,
                    "args": null,
                    "concreteType": "Instrument",
                    "plural": false,
                    "selections": [
                      (v7/*: any*/),
                      (v2/*: any*/)
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      (v8/*: any*/)
    ]
  },
  "params": {
    "operationKind": "query",
    "name": "AppAllLogsQuery",
    "id": null,
    "text": "query AppAllLogsQuery(\n  $num: Int!\n) {\n  allLogs(first: $num) {\n    edges {\n      node {\n        id\n        hasHourly\n        hasDaily\n        hasMonthly\n        dateCollected\n        instrument {\n          instrument\n          id\n        }\n      }\n    }\n  }\n  allInstruments(first: $num) {\n    edges {\n      node {\n        id\n        instrument\n        logs {\n          edges {\n            node {\n              id\n              dateCollected\n              hasHourly\n              hasDaily\n              hasMonthly\n            }\n          }\n        }\n      }\n    }\n  }\n}\n",
    "metadata": {}
  }
};
})();
// prettier-ignore
(node/*: any*/).hash = 'f9e6b73fc52774a8f8e66fe676e2a4b6';

module.exports = node;
