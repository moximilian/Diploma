<template>
    <TableCell>
        <input type="checkbox" class="custom-checkbox" @change="click" :checked="isChecked" />
    </TableCell>
</template>
<script>
export default {
    emits: ['clickCheckBox'],
    data() {
        return {
            isChecked: false,
        }
    },
    methods: {
        click() {
            this.isChecked = !this.isChecked
            this.$emit('clickCheckBox', this.isChecked)
        },
    },
}
</script>
