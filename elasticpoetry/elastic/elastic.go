package elastic

import (
	"io"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
	"github.com/golang/glog"
	jsoniter "github.com/json-iterator/go"
)

// elastics elastics
var elastics *elasticsearch.Client

const elasticTimeout = 10

// InitElastic 初始化Elastic
func InitElastic(domain, cacert, username, password string) bool {
	cert, err := os.ReadFile(cacert)
	if err != nil {
		glog.Info(err)
		return false
	}

	cfg := elasticsearch.Config{
		Addresses: []string{domain},
		Username:  username,
		Password:  password,
		CACert:    cert,
	}
	elastics, err = elasticsearch.NewClient(cfg)
	if err != nil {
		glog.Info(err)
		return false
	}

	res, err := elastics.Info()
	if err != nil {
		glog.Info(err)
		return false
	}
	defer res.Body.Close()
	if res.IsError() {
		glog.Info(err)
		return false
	}

	glog.Infof("ElasticSearch Server Open: username: %s, address: %+v\n", cfg.Username, cfg.Addresses)

	if !checkIndex([]string{"author", "poetry", "book"}) {
		glog.Info("indices is not exists")
		return false
	}

	return true
}

// checkIndex 检查索引是否存在，如果不存在就创建
func checkIndex(indices []string) bool {
	res, err := elastics.Indices.GetAlias()
	if err != nil {
		glog.Info(err)
		return false
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		glog.Info(res.String())
		return false
	}

	var mapIndex map[string]interface{}
	err = jsoniter.NewDecoder(res.Body).Decode(&mapIndex)
	if err != nil {
		glog.Info(err)
		return false
	}
	for _, index := range indices {
		if _, ok := mapIndex[index]; !ok {
			strValue := ""
			switch index {
			case "search_record":
				strValue = `{"mappings":{"properties":{"key":{"type":"completion","analyzer":"ik_smart"},"date":{"type":"date"},"resultType":{"type":"integer"},"results":{"type":"object","properties":{"isOffical":{"type":"boolean"},"title":{"type":"text"},"url":{"type":"text"},"note":{"type":"text"}}}}}}`
			case "gpt_record":
				strValue = `{"mappings":{"properties":{"key":{"type":"keyword"},"date":{"type":"date"},"resultType":{"type":"integer"},"results":{"type":"object","properties":{"isOffical":{"type":"boolean"},"title":{"type":"text"},"url":{"type":"text"},"note":{"type":"text"}}}}}}`
			case "ad_map":
				strValue = `{"mappings":{"properties":{"key":{"type":"text","analyzer":"ik_smart"},"isOffical":{"type":"boolean"},"title":{"type":"text"},"url":{"type":"text"},"note":{"type":"text"},"create_date":{"type":"date"},"type":{"type":"integer"},"counts":{"type":"integer"}}}}`
			case "url_list":
				strValue = `{"mappings":{"properties":{"url":{"type":"keyword"}}}}`
			default:
				continue
			}
			res, err = elastics.Indices.Create(
				index,
				elastics.Indices.Create.WithTimeout(elasticTimeout*time.Second),
				elastics.Indices.Create.WithBody(strings.NewReader(strValue)),
			)
			if err != nil {
				glog.Info(err)
				return false
			}

			if res.IsError() {
				glog.Info(res.String())
				return false
			}
		}
	}

	return true
}

// // insertDocument 创建文档
// func insertDocument(index string, document string, data []byte) bool {
// 	if len(data) <= 0 || len(index) <= 0 {
// 		return false
// 	}

// 	es := getEntiy()
// 	if es == nil {
// 		return false
// 	}

// 	res, err := es.Create(
// 		index,
// 		document,
// 		bytes.NewReader(data),
// 		es.Create.WithTimeout(elasticTimeout*time.Second),
// 	)
// 	if err != nil {
// 		glog.Info(err)
// 		return false
// 	}
// 	defer res.Body.Close()

// 	if res.IsError() {
// 		glog.Info(res.String())
// 		return false
// 	}
// 	return true
// }

// // updateDocument 更新文档
// func updateDocument(index string, document string, data []byte) bool {
// 	if len(data) <= 0 || len(index) <= 0 || len(document) <= 0 {
// 		return false
// 	}

// 	es := getEntiy()
// 	if es == nil {
// 		return false
// 	}

// 	res, err := es.Update(
// 		index,
// 		document,
// 		bytes.NewReader([]byte(fmt.Sprintf(`{"doc":%s}`, data))),
// 		es.Update.WithTimeout(elasticTimeout*time.Second),
// 	)
// 	if err != nil {
// 		glog.Info(err)
// 		return false
// 	}
// 	defer res.Body.Close()

// 	if res.IsError() {
// 		glog.Info(res.String())
// 		return false
// 	}
// 	return true
// }

// // getDocumentWithID 通过documentID获取文档
// func getDocumentWithID(index string, document string) []byte {
// 	if len(document) <= 0 || len(index) <= 0 {
// 		return nil
// 	}

// 	es := getEntiy()
// 	if es == nil {
// 		return nil
// 	}

// 	res, err := es.GetSource(
// 		index,
// 		document,
// 	)
// 	if err != nil {
// 		glog.Info(err)
// 		return nil
// 	}
// 	defer res.Body.Close()

// 	if res.IsError() {
// 		glog.Info(res.String())
// 		return nil
// 	}

// 	body, err := io.ReadAll(res.Body)
// 	if err != nil {
// 		glog.Info(err)
// 		return nil
// 	}
// 	return body
// }

// // searchDocument 搜索文档
// func searchDocument(index []string, key, field string) []byte {
// 	if len(index) <= 0 || len(key) <= 0 || len(field) <= 0 {
// 		return nil
// 	}

// 	es := getEntiy()
// 	if es == nil {
// 		return nil
// 	}

// 	res, err := es.Search(
// 		es.Search.WithIndex(index...),
// 		es.Search.WithQuery(field+":"+key),
// 		es.Search.WithFilterPath("hits.hits"),
// 		es.Search.WithSize(1),
// 		es.Search.WithTimeout(elasticTimeout*time.Second),
// 		// es.Search.WithPretty(),
// 	)
// 	if err != nil {
// 		glog.Info(err)
// 		return nil
// 	}
// 	defer res.Body.Close()

// 	if res.IsError() {
// 		glog.Info(res.String())
// 		return nil
// 	}

// 	body, err := io.ReadAll(res.Body)
// 	if err != nil {
// 		glog.Info(err)
// 		return nil
// 	}
// 	return body
// }

// analyzeKey 关键词分词
func analyzeKey(search string, filter []string) []byte {
	res, err := elastics.Indices.Analyze(
		// es.Indices.Analyze.WithIndex(key),
		elastics.Indices.Analyze.WithBody(strings.NewReader(search)),
		elastics.Indices.Analyze.WithFilterPath(filter...),
		elastics.Indices.Analyze.WithPretty(),
	)
	if err != nil {
		glog.Info(err)
		return nil
	}
	defer res.Body.Close()

	if res.IsError() {
		glog.Info(res.String())
		return nil
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		glog.Info(err)
		return nil
	}
	return body
}

// searchDocument 搜索文档
func searchDocument(index []string, search string, filter []string) []byte {
	if len(index) <= 0 || len(search) <= 0 {
		return nil
	}

	res, err := elastics.Search(
		elastics.Search.WithIndex(index...),
		elastics.Search.WithBody(strings.NewReader(search)),
		elastics.Search.WithFilterPath(filter...),
		elastics.Search.WithTimeout(elasticTimeout*time.Second),
		// es.Search.WithPretty(),
	)
	if err != nil {
		glog.Info(err)
		return nil
	}
	defer res.Body.Close()

	if res.IsError() {
		glog.Info(res.String())
		return nil
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		glog.Info(err)
		return nil
	}
	return body
}

// countDocument 统计文档数
func countDocument(index string) []byte {
	if len(index) <= 0 {
		return nil
	}

	res, err := elastics.Count(elastics.Count.WithIndex(index))
	if err != nil {
		glog.Info(err)
		return nil
	}
	defer res.Body.Close()

	if res.IsError() {
		glog.Info(res.String())
		return nil
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		glog.Info(err)
		return nil
	}
	return body
}

// bulkDocument 批处理
func bulkDocument(data string) {
	if len(data) <= 0 {
		return
	}

	res, err := elastics.Bulk(
		strings.NewReader(data),
		elastics.Bulk.WithTimeout(elasticTimeout*time.Second),
	)
	if err != nil {
		glog.Info(err)
		return
	}
	defer res.Body.Close()

	if res.IsError() {
		glog.Info(res.String())
		return
	}
}
