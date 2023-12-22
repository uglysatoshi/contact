<h1 align-items="center">Курсовая работа по проектированию IT-систем и мультимедийных приложений</h1>
<h3>Задание:</h3>
<p>Создание информационной системы для управления клиентской базой данных и автоматизации процесса продаж</p>

<h3> Иструкция по сборке </h3>

Перед выполнением комманд описанных ниже, необходимо установить MongoDB и запустить сервер.
Затем создать базу данных curse и две коллекции operators и clients

_operators_
```js
{
    id: ObjectID(''),
    email: "",
    password: "",
    firstname: "",
    lastname: "",
    title: "",
    manager: true/false,
    seller: true/false
}
```

_clients_
```js
{
    id: ObjectID(''),
    firstname: "",
    lastname: "",
    registration_date: "",
    balance: 0,
    purchases: 0
}
```

Сборка проекта:
```cmd
    git clone https://github.com/uglysatoshi/contact
    cd contact
    py -m venv .venv
    ./.venv/Scripts/activate
    pip install -r requirements.txt
    py run.py
 ```
