* 4 协程: 协程本质上是一种用户态的线程，不需要操作系统来进行抢占式调度，且在真正的实现中寄存于线程中，因此，系统开销极小，可以有效提高线程任务并发性，而避免多线程的缺点，使用协程的优点是编程简单，结构清晰；缺点是需要语言的支持，目前，原声支持协程的语言很少；
    协程也叫轻量级的线程，与传统的系统级线程相比，协程最大的优势在于“轻量级”，可以轻松创建上百万而不会导致系统资源衰竭，而线程和进程通常最多不能超过1万个。
# go语言的并发机制
  go支持轻量级线程，叫做goroutine。go语言标准库提供的所有系统调用操作，都会出让cpu给其他goroutine，让轻量级的线程切换管理不依赖于系统的线程和进程，也不依赖于cpu的核心数量；
  * 1 go 中goroutine的使用：
     ```
     func Add(x,y int){
        z := x + y
	fmt.Println(z)
     }
     
     go Add(1,1)
     ```
  * 2 goroutine中的并发通信：
     在工程上有两种最常见的并发通信模式：共享数据和消息。
     1.1 共享数据是指多个并发单元分别保持对同一个数据引用，实现对数据的共享，被共享的数据可能有多种形式，比如：*内存数据块、磁盘文件、网络数据等，*
     1.2 消息队列：线程间通过传递消息来实现通信；
     ```
        package main

	import "fmt"

	func Count(ch chan int){
		fmt.Println("Counting")
		ch <- 1
	}

	func main(){
		chs := make([]chan int,10)
		for index,_ := range chs {
			chs[index] = make(chan int)
			go Count(chs[index])
		}
		for _,ch := range chs {
			<- ch
		}
	}
     ```
     1.3 channel的使用
       - 声明：**var** chanName **chan** ElementType
               **var** m map[string] **chan** bool
       - 初始化：ch := **make**(**chan** int)//这就声明了一个类型为int类型的chan
       - 数据写入: ch <- 1
       - 数据读出：volue := <-ch
     1.4 select 搭配channel的使用
     ```
         select{
	     **case** <-chan1:
	     //如果chan1成功读取到数据，执行此快代码；
	     **case** chan2 >- 1:
	     //如果成功写入chan2中，执行此代码块；
	     **default**：
	     //默认执行此代码快；
	 }
     ```
     1.5 select 的特殊用法，随机向ch里面写入0、1;
     ```
         ch := make(chan int,1)
	 for {
	   select{
	      **case** ch <- 0:
	      **case** ch <- 1:
	   }
          }
	  i := <-ch
	  fmt.Println("Value received:",i)
      ```
      1.6 缓冲机制，创建一个带缓冲的channel
      ```
         c := make(chan int,1024)
	 //使用第二个参数传入即可创建一个带有缓冲的channel，即使没有数据读取时写入方也可以一直写入在缓冲区被填满之前都不会阻塞；
      ```
      1.7 超时机制，处理死锁现象
      ```
         //首先，我们并行一个匿名的超时等待函数
	 timeout := make(chan bool,1)
	 go func() {
	    time.Sleep(le9) //等待1秒钟；
	    timeout <- true
	 }()
	 //然后我们把timeout这个channel利用起来
	 select {
	    case <-ch:
	     //执行正常语句；
	    case <-timeout:
	     //一直没有从ch中读取到数据，但从timeout中读取到了
	 }
	```
	1.8 单项channel
	```
	 var ch1 chan int //ch1是一个正常的channel
         var ch2 chan<- float64 //ch2是一个单行的只用于写入的channel
	 var ch3 <-chan int //ch3是一个单向的只用于读取的channel

	 单项channel的作用：
	    保证最小原则，防止过多的权限导致的程序失控问题；
	 单向channel的初始化:
	  ch4 := make(chan int)
	  ch5 := <-chan int(ch4)
	  ch6 := chan <- int(ch4)
	```
	 1.9 关闭channel
	 ```
	 close(ch)
	 怎样判断channel是否关闭？
	 x,ok := <-ch
	 如果ok为false，表示channel已经关闭；
	 ```
          

