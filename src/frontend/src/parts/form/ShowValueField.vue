<template>
    <div class="show-field">
        <span class="title" :name="name">{{ title }}</span>   
        <div class="value-container">
            <span :name="name">{{ viewValue }}</span>
        </div>
    </div>
</template>
<script>
import InputPropsMixin from './help/props/InputPorpsMixin'

export default {
    mixins: [InputPropsMixin],
    computed: {
        viewValue() {
            if (this.value.length > 64) {
                const toDelete = this.value.substring(64, this.value.length)
                return this.value.replace(toDelete, '')  + '...'
            }
            return this.value
        }
    }
}
</script>
