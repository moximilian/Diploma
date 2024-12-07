<template>
    <div id="app">
        <main>
            <HeaderBar/>
            <router-view />
            {{ 'Welcome to my new Diploma!'  }}
        </main>
    </div>
</template>

<script>
export default {
    data() {
        return {
        }
    },
    methods: {
    },
}
</script>
