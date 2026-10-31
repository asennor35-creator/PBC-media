// Link WA berkode: pratamabuild.id/wa/K013 -> WhatsApp PBC dengan kode sumber, klik dicatat di pbc_wa_clicks (wa-k013)
add_action( 'template_redirect', function () {
	$path = trim( (string) parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ), '/' );
	if ( ! preg_match( '#^wa/([A-Za-z0-9-]{1,20})$#', $path, $m ) ) { return; }
	$code = strtoupper( $m[1] );
	if ( 0 !== strpos( $code, 'UJI' ) ) {
		$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? $_SERVER['REMOTE_ADDR'] : '';
		$key = 'pbc_wak_' . md5( $ip . $code );
		if ( ! get_transient( $key ) ) {
			set_transient( $key, 1, 30 );
			$src = 'wa-' . sanitize_key( $code );
			$day = current_time( 'Y-m-d' );
			$all = get_option( 'pbc_wa_clicks', array() );
			if ( ! is_array( $all ) ) { $all = array(); }
			if ( ! isset( $all[ $day ] ) ) { $all[ $day ] = array(); }
			$all[ $day ][ $src ] = ( isset( $all[ $day ][ $src ] ) ? $all[ $day ][ $src ] : 0 ) + 1;
			update_option( 'pbc_wa_clicks', $all, false );
		}
	}
	do_action( 'litespeed_control_set_nocache', 'pbc wa kode' );
	nocache_headers();
	$text = rawurlencode( 'Halo PBC, saya mau tanya soal proyek. (' . $code . ')' );
	wp_redirect( 'https://wa.me/6285745026574?text=' . $text, 302 );
	exit;
}, 5 );
