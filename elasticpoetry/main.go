package main

import (
	"elasticpoetry/elastic"
	"flag"

	"github.com/golang/glog"
)

func main() {
	//配置日志
	flag.Set("logtostderr", "true")
	flag.Set("stderrthreshold", "INFO")
	flag.Parse()
	defer glog.Flush()

	// 初始化Elastic
	if ok := elastic.InitElastic(
		"https://db.guangzhou.wangqianhong.com:19200",
		"/home/wqh/chinese-poetry/elasticpoetry/es_ca.crt",
		"elastic",
		"W*5rE#8@l7",
	); !ok {
		glog.Info("InitElastic failure")
		return
	}
}
