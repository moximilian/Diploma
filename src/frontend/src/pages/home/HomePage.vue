<template>
    <div>
        <h1>Welcome to the Home Page</h1>
        <p>This is the index page.</p>
        <router-link to="/auth/login">Go to Login</router-link>
    </div>
</template>
  
<script>
export default {
    name: "HomePage",
    };
</script>