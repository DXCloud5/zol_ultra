# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
'''编号列表     对应rule
1：CPU           0
2：显卡 vga      1
3：主板 board    2
4：硬盘 disk     3-6
5：内存 memory   6
6：电源 power    7
7：散热 heat     8
8：机箱 box      9
'''

class GetPartsListSpider(CrawlSpider):
    name = 'get_parts_list'
    allowed_domains = ['zol.com.cn']
    start_urls = ['http://detail.zol.com.cn/cpu/s6219/hot.html',#台式机CPU
                  'http://detail.zol.com.cn/vga/hot.html',#这里不分发烧级 主流级 和 入门级 这些参数可以在详情页获取
                  'http://detail.zol.com.cn/motherboard/hot.html',
                  'http://detail.zol.com.cn/hard_drives/s1866/hot.html',
                  'http://detail.zol.com.cn/solid_state_drive/s8137/hot.html',
                  'http://detail.zol.com.cn/solid_state_drive/s2638/hot.html',#HDD SATA3 和 SDD SATA3 和M.2 PCIE
                  'http://detail.zol.com.cn/memory/s5974_p26895/hot.html', #台式机 ddr4
                  'http://detail.zol.com.cn/power/s6568/hot.html',#台式机电源 不包含游戏电源
                  'http://detail.zol.com.cn/cooling_product/p831/hot.html',#CPU散热器
                  'http://detail.zol.com.cn/case/hot.html'
                  ]

    rules = (
        Rule(LinkExtractor(allow=start_urls[0]), callback='parse_CPU'),
        #Rule(LinkExtractor(allow=start_urls[1]), callback='parse_vga'),
        #Rule(LinkExtractor(allow=start_urls[2]), callback='parse_board'),
        #Rule(LinkExtractor(allow=start_urls[3:6]), callback='parse_disk'),
        #Rule(LinkExtractor(allow=start_urls[6]), callback='parse_memory'),
        #Rule(LinkExtractor(allow=start_urls[7]), callback='parse_power'),
        #Rule(LinkExtractor(allow=start_urls[8]), callback='parse_heat'),
        #Rule(LinkExtractor(allow=start_urls[9]), callback='parse_box'),
    )
    count1 = count2 = count3 = count4 = count5 = count6 = count7 = count8 = 0#关于翻页：在实际应用中，前几页的热门数据基本已经可以满足实际需求
    '''
    主体：获取产品url；  a：获取参数url；  b：获取详细信息
    '''
    #1
    def parse_CPU(self, response):
        url_list = response.xpath('//ul[@id="J_PicMode"]//li/a/@href').extract()
        next_url = response.xpath('//div[@class="pagebar"]//a[@class="next"]/@href').extract()[0]
        next_url = "http://detail.zol.com.cn" + next_url
        self.count1 +=1
        if(self.count1 <5):
            yield scrapy.Request(
                next_url,
                callback=self.parse_CPU,
                dont_filter=True,
            )
        for i in url_list:
            yield scrapy.Request(
                "http://detail.zol.com.cn" + i,
                callback=self.parse_CPU_a,
            )
    def parse_CPU_a(self, response):
        url = response.xpath('//div[@id="_j_tag_nav"]//li/a[contains(text(), "参数")]/@href').extract()[0]

        yield scrapy.Request(
            "http://detail.zol.com.cn" + url,
            callback=self.parse_CPU_b,
        )
    def parse_CPU_b(self, response):
        CPU_detail = {}
        CPU_detail['index'] = 1
        id = ''
        CPU_detail['产品名称'] = response.xpath('//div[@class="breadcrumb"]/a[@target="_self"]//text()').extract()[0]

        # CPU_detail['key'] = response.xpath('//tr//th//span//text()').extract()
        # CPU_detail['value'] = response.xpath('//tr//td[@class="hover-edit-param"]//span//text()').extract()
            # ['适用类型：', '台式机', 'CPU系列：', 'Ryzen 9', 'CPU主频：', '3.8GHz', '动态 加速频率：', '4.6GHz', '插槽类型：', 'Socket AM4', '二级缓存：', '6MB', '核心数量：', '十二核心', '线程数：', '二十四线程']
            # CPU_detail['重要参数'] = response.xpath('//div[@class="section-content"]//p//text()').extract() #不统一，无参考价值
            # re: match( @class ,'allstar\d0 ')   r = response.xpath('//a[contains(text(), ".mkv")]/@href').extract()

        CPU_detail['价格'] = response.xpath('//div[@class="goods-card__price"]/span/text()').extract()[0]

        TDP_id_list = response.xpath('//tr//th//span[contains(text(),"热设计功耗")]//@id').extract()
        if len(TDP_id_list) > 0:
            TDP_id = TDP_id_list[0]
            id = TDP_id.split("_")[1]
            CPU_detail['TDP'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            CPU_detail['TDP'] = "NULL"
        socket_id_list = response.xpath('//tr//th//span[contains(text(),"插槽类型")]//@id').extract()
        if len(socket_id_list) > 0:
            socket_id = socket_id_list[0]
            id = socket_id.split("_")[1]
            CPU_detail['插槽'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            CPU_detail['插槽'] = "NULL"
        vision_id_list = response.xpath('//tr//th//span[contains(text(),"集成显卡")]//@id').extract()
        if len(vision_id_list) > 0:
            vision_id = vision_id_list[0]
            id = vision_id.split("_")[1]
            CPU_detail['显卡'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            CPU_detail['显卡'] = '不支持'

        yield CPU_detail
    #2
    def parse_vga(self, response):
        url_list = response.xpath('//ul[@id="J_PicMode"]//li/a/@href').extract()
        next_url = response.xpath('//div[@class="pagebar"]//a[@class="next"]/@href').extract()[0]
        next_url = "http://detail.zol.com.cn" + next_url
        #print(next_url)
        self.count2 += 1
        if(self.count2 < 5):
            yield scrapy.Request(
                next_url,
                callback=self.parse_vga,
                dont_filter=True,
            )
        for i in url_list:
            yield scrapy.Request(
                "http://detail.zol.com.cn" + i,
                callback=self.parse_vga_a,
            )
    def parse_vga_a(self, response):
        url = response.xpath('//div[@id="_j_tag_nav"]//li/a[contains(text(), "参数")]/@href').extract()[0]

        yield scrapy.Request(
            "http://detail.zol.com.cn" + url,
            callback=self.parse_vga_b,
        )
    def parse_vga_b(self, response):
        vga_detail = {}
        vga_detail['index'] = 2
        id = ''
        vga_detail['产品名称'] = response.xpath('//div[@class="breadcrumb"]/a[@target="_self"]//text()').extract()[0]

        vga_detail['价格'] = response.xpath('//div[@class="goods-card__price"]/span/text()').extract()[0]

        TDP_id_list = response.xpath('//tr//th//span[contains(text(),"最大功耗")]//@id').extract()
        if len(TDP_id_list) > 0:
            TDP_id = TDP_id_list[0]
            id = TDP_id.split("_")[1]
            vga_detail['TDP'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            vga_detail['TDP'] = 'NULL'

        power_id_list1 = response.xpath('//tr//th//span[contains(text(),"建议电源")]//@id').extract()
        if len(power_id_list1) > 0:
            power_id = power_id_list1[0]
            id = power_id.split("_")[1]
            vga_detail['建议电源'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            vga_detail['建议电源'] = 'NULL'

        level_id_list = response.xpath('//tr//th//span[contains(text(),"显卡类型")]//@id').extract()
        if len(level_id_list) > 0:
            level_id = level_id_list[0]
            id = level_id.split("_")[1]
            vga_detail['显卡类型'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            vga_detail['显卡类型'] = 'NULL'
        yield vga_detail
    #3
    def parse_board(self, response):
        url_list = response.xpath('//ul[@id="J_PicMode"]//li/a/@href').extract()
        next_url = response.xpath('//div[@class="pagebar"]//a[@class="next"]/@href').extract()[0]
        next_url = "http://detail.zol.com.cn" + next_url
        #print(next_url)
        self.count3 += 1
        if(self.count3 > 5):
            yield scrapy.Request(
                next_url,
                callback=self.parse_board,
                dont_filter=True,
            )
        for i in url_list:
            yield scrapy.Request(
                "http://detail.zol.com.cn" + i,
                callback=self.parse_board_a,
            )
    def parse_board_a(self, response):
        url = response.xpath('//div[@id="_j_tag_nav"]//li/a[contains(text(), "参数")]/@href').extract()[0]

        yield scrapy.Request(
            "http://detail.zol.com.cn" + url,
            callback=self.parse_board_b,
        )
    def parse_board_b(self, response):
        board_detail = {}
        board_detail['index'] = 3
        id = ''
        board_detail['产品名称'] = response.xpath('//div[@class="breadcrumb"]/a[@target="_self"]//text()').extract()[0]

        board_detail['价格'] = response.xpath('//div[@class="goods-card__price"]/span/text()').extract()[0]

        socket_id_list = response.xpath('//tr//th//span[contains(text(),"CPU插槽")]//@id').extract()
        if len(socket_id_list) > 0:
            socket_id = socket_id_list[0]
            id = socket_id.split("_")[1]
            board_detail['CPU插槽'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            board_detail['CPU插槽'] = 'NULL'

        model_id_list1 = response.xpath('//tr//th//span[contains(text(),"主板板型")]//@id').extract()
        if len(model_id_list1) > 0:
            model_id = model_id_list1[0]
            id = model_id.split("_")[1]
            board_detail['主板板型'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            board_detail['主板板型'] = 'NULL'

        core_id_list = response.xpath('//tr//th//span[contains(text(),"主芯片组")]//@id').extract()
        if len(core_id_list) > 0:
            core_id = core_id_list[0]
            id = core_id.split("_")[1]
            board_detail['主芯片组'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            board_detail['主芯片组'] = 'NULL'
        yield board_detail
    #4
    def parse_disk(self, response):
        url_list = response.xpath('//ul[@id="J_PicMode"]//li/a/@href').extract()
        next_url = response.xpath('//div[@class="pagebar"]//a[@class="next"]/@href').extract()[0]
        next_url = "http://detail.zol.com.cn" + next_url
        #print(next_url)
        self.count4 += 1
        if(self.count4 > 10):
            yield scrapy.Request(
                next_url,
                callback=self.parse_disk,
                dont_filter=True,
            )
        for i in url_list:
            yield scrapy.Request(
                "http://detail.zol.com.cn" + i,
                callback=self.parse_disk_a,
            )
    def parse_disk_a(self, response):
        url = response.xpath('//div[@id="_j_tag_nav"]//li/a[contains(text(), "参数")]/@href').extract()[0]

        yield scrapy.Request(
            "http://detail.zol.com.cn" + url,
            callback=self.parse_disk_b,
        )
    def parse_disk_b(self, response):
        disk_detail = {}
        id = ''
        disk_detail['index'] = 4
        disk_detail['产品名称'] = response.xpath('//div[@class="breadcrumb"]/a[@target="_self"]//text()').extract()[0]

        disk_detail['价格'] = response.xpath('//div[@class="goods-card__price"]/span/text()').extract()[0]

        cap_id_list = response.xpath('//tr//th//span[contains(text(),"容量")]//@id').extract()
        if len(cap_id_list) > 0:
            cap_id = cap_id_list[0]
            id = cap_id.split("_")[1]
            disk_detail['容量'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            disk_detail['容量'] = 'NULL'

        cache_id_list1 = response.xpath('//tr//th//span[contains(text(),"缓存")]//@id').extract()
        if len(cache_id_list1) > 0:
            cache_id = cache_id_list1[0]
            id = cache_id.split("_")[1]
            disk_detail['缓存'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            disk_detail['缓存'] = 'NULL'

        socket_id_list = response.xpath('//tr//th//span[contains(text(),"接口类型")]//@id').extract()
        if len(socket_id_list) > 0:
            socket_id = socket_id_list[0]
            id = socket_id.split("_")[1]
            disk_detail['接口类型'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            disk_detail['接口类型'] = 'NULL'

        read_id_list = response.xpath('//tr//th//span[contains(text(),"读取速度")]//@id').extract()
        if len(read_id_list) > 0:
            read_id = read_id_list[0]
            id = read_id.split("_")[1]
            disk_detail['读取速度'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            disk_detail['读取速度'] = 'NULL'

        write_id_list = response.xpath('//tr//th//span[contains(text(),"写入速度")]//@id').extract()
        if len(write_id_list) > 0:
            write_id = write_id_list[0]
            id = write_id.split("_")[1]
            disk_detail['写入速度'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            disk_detail['写入速度'] = 'NULL'
        yield disk_detail
    #5
    def parse_memory(self, response):
        url_list = response.xpath('//ul[@id="J_PicMode"]//li/a/@href').extract()
        next_url = response.xpath('//div[@class="pagebar"]//a[@class="next"]/@href').extract()[0]
        next_url = "http://detail.zol.com.cn" + next_url
        self.count5 += 1
        if (self.count5 < 5):
            yield scrapy.Request(
                next_url,
                callback=self.parse_memory,
                dont_filter=True,
            )
        for i in url_list:
            yield scrapy.Request(
                "http://detail.zol.com.cn" + i,
                callback=self.parse_memory_a,
            )
    def parse_memory_a(self, response):
        url = response.xpath('//div[@id="_j_tag_nav"]//li/a[contains(text(), "参数")]/@href').extract()[0]

        yield scrapy.Request(
            "http://detail.zol.com.cn" + url,
            callback=self.parse_memory_b,
        )
    def parse_memory_b(self, response):
        memory_detail = {}
        id = ''
        memory_detail['index'] = 5
        memory_detail['产品名称'] = response.xpath('//div[@class="breadcrumb"]/a[@target="_self"]//text()').extract()[0]

        memory_detail['价格'] = response.xpath('//div[@class="goods-card__price"]/span/text()').extract()[0]

        capacity_id_list1 = response.xpath('//tr//th//span[contains(text(),"内存容量")]//@id').extract()
        if len(capacity_id_list1) > 0:
            capacity_id = capacity_id_list1[0]
            id = capacity_id.split("_")[1]
            memory_detail['内存容量'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            memory_detail['内存容量'] = 'NULL'

        frequency_id_list = response.xpath('//tr//th//span[contains(text(),"内存主频")]//@id').extract()
        if len(frequency_id_list) > 0:
            frequency_id = frequency_id_list[0]
            id = frequency_id.split("_")[1]
            memory_detail['内存主频'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            memory_detail['内存主频'] = 'NULL'
        yield memory_detail
    #6
    def parse_power(self, response):
        url_list = response.xpath('//ul[@id="J_PicMode"]//li/a/@href').extract()
        next_url = response.xpath('//div[@class="pagebar"]//a[@class="next"]/@href').extract()[0]
        next_url = "http://detail.zol.com.cn" + next_url
        self.count6 += 1
        if (self.count6 < 4):
            yield scrapy.Request(
                next_url,
                callback=self.parse_power,
                dont_filter=True,
            )
        for i in url_list:
            yield scrapy.Request(
                "http://detail.zol.com.cn" + i,
                callback=self.parse_power_a,
            )
    def parse_power_a(self, response):
        url = response.xpath('//div[@id="_j_tag_nav"]//li/a[contains(text(), "参数")]/@href').extract()[0]

        yield scrapy.Request(
            "http://detail.zol.com.cn" + url,
            callback=self.parse_power_b,
        )
    def parse_power_b(self, response):
        power_detail = {}
        id = ''
        power_detail['index'] = 6
        power_detail['产品名称'] = response.xpath('//div[@class="breadcrumb"]/a[@target="_self"]//text()').extract()[0]

        power_detail['价格'] = response.xpath('//div[@class="goods-card__price"]/span/text()').extract()[0]

        TDP_id_list = response.xpath('//tr//th//span[contains(text(),"额定功率")]//@id').extract()
        if len(TDP_id_list) > 0:
            TDP_id = TDP_id_list[0]
            id = TDP_id.split("_")[1]
            power_detail['额定功率'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            power_detail['额定功率'] = 'NULL'

        size_id_list1 = response.xpath('//tr//th//span[contains(text(),"电源尺寸")]//@id').extract()
        if len(size_id_list1) > 0:
            size_id = size_id_list1[0]
            id = size_id.split("_")[1]
            power_detail['电源尺寸'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            power_detail['电源尺寸'] = 'NULL'

        auth_id_list = response.xpath('//tr//th//span[contains(text(),"80PLUS认证")]//@id').extract()
        if len(auth_id_list) > 0:
            auth_id = auth_id_list[0]
            id = auth_id.split("_")[1]
            power_detail['80PLUS认证'] = \
            response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            power_detail['80PLUS认证'] = 'NULL'
        yield power_detail
    #7
    def parse_heat(self, response):
        url_list = response.xpath('//ul[@id="J_PicMode"]//li/a/@href').extract()
        next_url = response.xpath('//div[@class="pagebar"]//a[@class="next"]/@href').extract()[0]
        next_url = "http://detail.zol.com.cn" + next_url
        self.count7 += 1
        if (self.count7 < 5):
            yield scrapy.Request(
                next_url,
                callback=self.parse_heat,
                dont_filter=True,
            )
        for i in url_list:
            yield scrapy.Request(
                "http://detail.zol.com.cn" + i,
                callback=self.parse_heat_a,
            )
    def parse_heat_a(self, response):
        url = response.xpath('//div[@id="_j_tag_nav"]//li/a[contains(text(), "参数")]/@href').extract()[0]

        yield scrapy.Request(
            "http://detail.zol.com.cn" + url,
            callback=self.parse_heat_b,
        )
    def parse_heat_b(self, response):
        heatkiller_detail = {}
        id = ''
        heatkiller_detail['index'] = 7
        heatkiller_detail['产品名称'] = response.xpath('//div[@class="breadcrumb"]/a[@target="_self"]//text()').extract()[0]

        heatkiller_detail['价格'] = response.xpath('//div[@class="goods-card__price"]/span/text()').extract()[0]

        method_id_list = response.xpath('//tr//th//span[contains(text(),"散热方式")]//@id').extract()
        if len(method_id_list) > 0:
            method_id = method_id_list[0]
            id = method_id.split("_")[1]
            heatkiller_detail['散热方式'] = \
                response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()
        else:
            heatkiller_detail['散热方式'] = 'NULL'

        socket_id_list1 = response.xpath('//tr//th//span[contains(text(),"适用范围")]//@id').extract()
        if len(socket_id_list1) > 0:
            socket_id = socket_id_list1[0]
            id = socket_id.split("_")[1]
            heatkiller_detail['适用范围'] = \
                response.xpath('//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()
        else:
            heatkiller_detail['适用范围'] = 'NULL'

        size_id_list = response.xpath('//tr//th//span[contains(text(),"产品尺寸")]//@id').extract()
        if len(size_id_list) > 0:
            size_id = size_id_list[0]
            id = size_id.split("_")[1]
            heatkiller_detail['产品尺寸'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            heatkiller_detail['产品尺寸'] = 'NULL'

        yield heatkiller_detail# 没法获取换行的text() 有一定数据缺失 换成list数据不缺失 但是有多余字符

    #8
    def parse_box(self, response):
        url_list = response.xpath('//ul[@id="J_PicMode"]//li/a/@href').extract()
        next_url = response.xpath('//div[@class="pagebar"]//a[@class="next"]/@href').extract()[0]
        next_url = "http://detail.zol.com.cn" + next_url
        self.count8 += 1
        if (self.count8 < 5):
            yield scrapy.Request(
                next_url,
                callback=self.parse_box,
                dont_filter=True,
            )
        for i in url_list:
            yield scrapy.Request(
                "http://detail.zol.com.cn" + i,
                callback=self.parse_box_a,
            )
    def parse_box_a(self, response):
        url = response.xpath('//div[@id="_j_tag_nav"]//li/a[contains(text(), "参数")]/@href').extract()[0]

        yield scrapy.Request(
            "http://detail.zol.com.cn" + url,
            callback=self.parse_box_b,
        )
    def parse_box_b(self, response):
        case_detail = {}
        id = ''
        case_detail['index'] = 8
        case_detail['产品名称'] = response.xpath('//div[@class="breadcrumb"]/a[@target="_self"]//text()').extract()[0]

        case_detail['价格'] = response.xpath('//div[@class="goods-card__price"]/span/text()').extract()[0]

        type_id_list = response.xpath('//tr//th//span[contains(text(),"机箱类型")]//@id').extract()
        if len(type_id_list) > 0:
            type_id = type_id_list[0]
            id = type_id.split("_")[1]
            case_detail['机箱类型'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            case_detail['机箱类型'] = 'NULL'

        struct_id_list1 = response.xpath('//tr//th//span[contains(text(),"机箱结构")]//@id').extract()
        if len(struct_id_list1) > 0:
            struct_id = struct_id_list1[0]
            id = struct_id.split("_")[1]
            case_detail['机箱结构'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            case_detail['机箱结构'] = 'NULL'

        board_id_list = response.xpath('//tr//th//span[contains(text(),"适用主板")]//@id').extract()
        if len(board_id_list) > 0:
            board_id = board_id_list[0]
            id = board_id.split("_")[1]
            case_detail['适用主板'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            case_detail['适用主板'] = 'NULL'

        vga_id_list = response.xpath('//tr//th//span[contains(text(),"显卡限长")]//@id').extract()
        if len(vga_id_list) > 0:
            vga_id = vga_id_list[0]
            id = vga_id.split("_")[1]
            case_detail['显卡限长'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            case_detail['显卡限长'] = 'NULL'

        heat_id_list = response.xpath('//tr//th//span[contains(text(),"散热器限高")]//@id').extract()
        if len(heat_id_list) > 0:
            heat_id = heat_id_list[0]
            id = heat_id.split("_")[1]
            case_detail['散热器限高'] = \
                response.xpath(
                    '//tr//td[@class="hover-edit-param"]//span[@id="newPmVal_' + id + '"]//text()').extract()[0]
        else:
            case_detail['散热器限高'] = 'NULL'
        yield case_detail

