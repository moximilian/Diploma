<template>
    <div class="monthPicker" :class="{ opened }">
        <div class="monthPicker-selected control-input" @click="toggle">
            {{ currentMonth }}
        </div>
        <div v-if="opened" class="monthPicker-popup">
            <div class="months">
                <div
                    v-for="(month, i) in months"
                    :key="i"
                    class="month"
                    :class="{ selected: isSelectedMonth(i) }"
                    @click="selectMonth(i, $event)"
                >
                    {{ month }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import mitt from 'mitt'
import { addGroupEventListeners } from '@/core/functions'
const emitter = mitt()

export default {
    props: {
        current: { type: Object, default: null },
    },
    emits: ['setMonth'],
    inject: ['setChildOpened'],
    data() {
        return {
            opened: false,
            monthsLabels: [
                'Январь',
                'Февраль',
                'Март',
                'Апрель',
                'Май',
                'Июнь',
                'Июль',
                'Август',
                'Сентябрь',
                'Октябрь',
                'Ноябрь',
                'Декабрь',
            ],
        }
    },
    computed: {
        currentMonth() {
            let m = this.monthsLabels[this.current.m]
            return m + ' ' + this.current.y
        },
        months() {
            return [...Array(12)].map((_, i) => this.monthsLabels[i])
        },
    },
    methods: {
        close() {
            this.opened = false
            this.setChildOpened(this.opened)
        },
        toggle() {
            this.opened = !this.opened
            this.setChildOpened(this.opened)
        },
        isSelectedMonth(month) {
            return month === this.current.m
        },
        selectMonth(month, e) {
            e.stopPropagation()
            this.$emit('setMonth', this.current.y, month)
            this.close()
        },
    },
    mounted() {
        emitter.on(
            'hook:beforeDestroy',
            addGroupEventListeners(document, {
                click: e => this.opened && !this.$el.contains(e.target) && this.close(e),
                keydown: e => e.code === 'Escape' && this.opened && this.close(e),
            }).abort
        )
    },
}
</script>
