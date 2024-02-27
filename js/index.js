const express = require('express')
const sequelize = require('./util/database')
const User = require('./models/users')
const axios = require('axios');

const app = express()
app.use(express.json())
const port = 3000

app.get('/', (req, res) => {
    res.send('Hello World')
})

app.post('/users', async(req, res) =>{
    try{
        const user = await User.create({
            username: req.body.username,
            email: req.body.email
        })
        return res.status(201).json(user);
    }catch (error){
        return res.status(500).json(error);
    }
})

app.get('/users-list', async(req, res) => {
    try {
        // Lógica para obter a lista de usuários (sua implementação)
        const users = await User.findAll();  // Exemplo: Usando Sequelize para consultar usuários

        // Retornar a lista de usuários como resposta
        return res.status(200).json(users);
    } catch (error) {
        console.error('Erro ao obter a lista de usuários:', error.message);
        return res.status(500).json({ error: 'Erro interno do servidor' });
    }
})

app.listen(port, () => {
    console.log(`App esta funcionando em http://localhost:${port}`)
})

sequelize.sync({force:false})
.then(() => app.listen(process.env.EXTERNALPORT))
.catch(err => log.error(err))