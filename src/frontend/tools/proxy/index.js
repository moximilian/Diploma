/**
 * Запуск прокси сервера
 *
 * npm run proxy
 * @argv[2] (serve) флаг для запуска дев-сервера вместе с прокси-сервером
 */

require('dotenv').config({ path: '.env.development.local', override: true })
require('dotenv').config({ path: '.env.development' })

const http = require('http')
const { spawn } = require('child_process')

const hostname = process.env.VUE_APP_PROXY.slice(7).split(':')[0]
const port = process.env.VUE_APP_PROXY.slice(7).split(':')[1]

process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0

const express = require('express')
const cors = require('cors')
const app = express()

const server = http.createServer(async (req, res) => {
    const url = process.env.VUE_APP_PROXY_API + req.url
    const resHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': '*',
    }

    req.on('data', async body => {
        req.headers['content-length'] = Buffer.byteLength(body)

        const data = await fetch(url, {
            method: req.method,
            headers: {
                ...req.headers,
            },
            body,
        }).then(response => {
            console.log(`\x1b[34mResponse ${url} | status ${response.statusText}\x1b[0m`)

            res.writeHead(response.status, {
                ...resHeaders,
                ...response.headers,
            })

            return response.text()
        })
        res.end(data)
    })
    if (req.method === 'OPTIONS') {
        res.writeHead(200, resHeaders)
        res.end('')
    }
})

async function init() {
    app.use(cors()) // Enable CORS for all routes

    server.listen(port, hostname, () => {
        console.log(`Прокси запущен на ${hostname}:${port}`)
    })

    if (process.argv[2] === 'serve') {
        const command = spawn('npm run', ['serve'], { shell: true })
        command.stdout.on('data', output => {
            console.info('Output: ', output.toString())
        })
    }
}

init()
