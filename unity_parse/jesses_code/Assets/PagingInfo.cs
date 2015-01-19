public class PagingInfo : object {

	public int PageIndex = 0;
	public int PageSize = 1000;

	public int SkipAmount {
		get {return this.PageSize * this.PageIndex; }
	}

}
