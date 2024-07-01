package elastic

type PoetryStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//作者
	Author string `json:"author"`
	//内容
	Cotent []string `json:"cotent"`
	//标签
	Tags []string `json:"tags,omitempty"`
}

type AuthorSturct struct {
	//ID
	ID string `json:"id"`
	//作者
	Author string `json:"author"`
	//作者简介
	Desc string `json:"desc,omitempty"`
}

// 作者介绍
type TangShiAuthorStruct struct {
	//作者
	Name string `json:"name"`
	//作者简介
	Desc string `json:"desc"`
}

// 作者介绍
type SongCiAuthortruct struct {
	//作者
	Name string `json:"name"`
	//作者简介
	Desc string `json:"description"`
}

// 曹操
type CaoCaoStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//作者
	Author string `json:"author"`
	//内容
	Paragraphs []string `json:"paragraphs"`
}

// 楚辞
type ChuCiStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//作者
	Author string `json:"author"`
	//内容
	Cotent []string `json:"cotent"`
	//副标题
	Section string `json:"section,omitempty"`
	//标签
	Tags []string `json:"tags,omitempty"`
}

// 论语
type LunYuStruct struct {
	//ID
	ID string `json:"id"`
	//章节
	Chapter string `json:"chapter"`
	//作者
	Author string `json:"author"`
	//内容
	Paragraphs []string `json:"paragraphs"`
	//标签
	Tags []string `json:"tags,omitempty"`
}

// 纳兰性德
type LLXDStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//作者
	Author string `json:"author"`
	//内容
	Para []string `json:"para"`
	//标签
	Tags []string `json:"tags,omitempty"`
}

// 唐宋诗
type TangSongShiStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//作者
	Author string `json:"author"`
	//内容
	Paragraphs []string `json:"paragraphs"`
	//标签
	Tags []string `json:"tags"`
}

// 诗经
type ShiJingStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//章节
	Chapter string `json:"chapter"`
	//副标题
	Section string `json:"section,omitempty"`
	//内容
	Cotent []string `json:"cotent"`
	//标签
	Tags []string `json:"tags,omitempty"`
}

// 宋词
type SongCiStruct struct {
	//ID
	ID string `json:"id"`
	//词牌
	Rhythmic string `json:"rhythmic"`
	//作者
	Author string `json:"author"`
	//内容
	Paragraphs []string `json:"paragraphs"`
	//标签
	Tags []string `json:"tags"`
}

// 五代
type WuDaiStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//作者
	Author string `json:"author"`
	//内容
	Paragraphs []string `json:"paragraphs"`
	//标签
	Tags []string `json:"tags"`
	//词牌
	Rhythmic string `json:"rhythmic,omitempty"`
	//注释
	Notes string `json:"notes,omitempty"`
}

// 幽梦影
type YouMengYingStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//作者
	Author string `json:"author"`
	//内容
	Content string `json:"content"`
	//评论
	Comment []string `json:"comment"`
	//标签
	Tags []string `json:"tags"`
}

// 元曲
type YuanQuStruct struct {
	//ID
	ID string `json:"id"`
	//标题
	Title string `json:"title"`
	//作者
	Author string `json:"author"`
	//内容
	Paragraphs []string `json:"paragraphs"`
	//标签
	Tags []string `json:"tags"`
}
