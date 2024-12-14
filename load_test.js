import http from 'k6/http';
import { check } from 'k6';

export let options = {
    stages: [
        { duration: '1m', target: 100 },  
        { duration: '3m', target: 500 }, 
        { duration: '3m', target: 1000 }, 
        { duration: '1m', target: 0 },   
    ],
};

export default function () {
  let res = http.get('http://localhost:8501');
  check(res, { 'status was 200': (r) => r.status === 200 });
}