<template>
    <div id="app">
        <main>
            <router-view />
            <!-- Место для отображения маршрутов -->
        </main>
    </div>
</template>

<script>
export default {
    name: 'App',
    // Вы можете добавить данные, методы, вычисляемые свойства и т.д.
    data() {
        return {
            // Пример данных
        }
    },
    methods: {
        // Пример методов
    },
}
</script>

<style>
/* Пример стилей */
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
