<template>
    <div class="timetable-day">
        <div
            class="block"
            v-for="index of blocks"
            :key="index"
            :style="{ height: blockSizeMins + 'px' }"
        >
            <div class="block" v-if="index % blocksInHour == 0 && currentTimeBlock !== index">
                <div class="semi-transparent-black-color" v-if="isShowHours">
                    {{ getHour(index) }}
                </div>
                <div class="line"></div>
            </div>
            <div class="block" v-if="currentTimeBlock === index">
                <div class="main-color" v-if="isShowHours">{{ new Date().toShowTime() }}</div>
                <div
                    class="line-current-time"
                    :class="{ ['semi-transparent']: !isShowCurrTimeLine }"
                ></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        currentDay: { type: Array, default: () => [] },
        blockSizeMins: { type: Number, default: () => 10 },
        isShowHours: { type: Boolean, default: () => true },
        isShowCurrTimeLine: { type: Boolean, default: () => true },
    },
    data() {
        return {
            blocksInHour: 10,
        }
    },
    methods: {
        getHour(index) {
            let hours = (index / this.blocksInHour + 1) % 24
            if (hours.toString().length === 1) hours = `0${hours}`
            return `${hours}:00`
        },
    },
    computed: {
        blocks() {
            return [...Array(24 * this.blocksInHour).keys()]
        },
        currentTimeBlock() {
            const date = new Date()
            const hours = date.getHours()
            let newIndex = (hours - 1) * this.blocksInHour
            const mins = date.getMinutes()
            newIndex += (mins % this.blocksInHour) + 1
            return newIndex + 1
        },
    },
    created() {
        this.blocksInHour = 60 / this.blockSizeMins
        
    },
}
</script>
