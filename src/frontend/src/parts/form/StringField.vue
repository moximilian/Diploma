<template>
    <InputField type="text" ref="inputField">
        <template #beforeInput="props">
            <slot name="beforeInput" v-bind="props"></slot>
        </template>
        <template #afterInput="props">
            <slot name="afterInput" v-bind="props"></slot>
        </template>
    </InputField>
</template>
