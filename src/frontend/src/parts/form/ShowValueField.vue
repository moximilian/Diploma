<template>
    <div class="value-container">
        <span :name="name">{{ value }}</span>
    </div>
</template>
<script>
import InputPropsMixin from './help/props/InputPorpsMixin'

export default {
    mixins: [InputPropsMixin],
}
</script>
