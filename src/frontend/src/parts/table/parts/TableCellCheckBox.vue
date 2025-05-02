<template>
    <TableCell>
        <input type="checkbox" class="custom-checkbox" @change="click" :checked="isChecked" />
    </TableCell>
</template>
<script>
export default {
    props: {
        isCheckedDefault: {type: Boolean, default: () => false}
    },
    emits: ['clickCheckBox'],
    data() {
        return {
            isChecked: this.isCheckedDefault,
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
