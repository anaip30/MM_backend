const http = require('http')

const server = http.createServer((req, res) => {
 if(req.url === '/'){
    res.end('welcomeeeeeeeeeeee')
 }
 if(req.url === '/about'){
    res.end('here nesto nesto')
 }
 res.end(`
   <h1>oooo<h1>
   <p> we we we we <p>
   <a href = "/">bacck</a>`
 )
})

server.listen(5001)