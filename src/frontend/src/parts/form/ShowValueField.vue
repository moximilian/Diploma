<template>
    <div class="show-field">
        <span class="title" :name="name">{{ title }}</span>   
        <div class="value-container">
            <span :name="name">{{ value }}</span>
        </div>
    </div>
</template>
<script>
import InputPropsMixin from './help/props/InputPorpsMixin'

export default {
    mixins: [InputPropsMixin],
}
</script>
