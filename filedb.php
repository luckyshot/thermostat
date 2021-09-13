<?php

/*
File Database Class
Avoid the use of MySQL by storing variables and arrays into readable files
Version: 1.0.2
Usage:
    require 'filedb.php';
	$fdb = new FileDB;
	$data = $fdb->get( 'data' );
	$fdb->set( 'data', $data );
	if ( !$data ){
		$data = [
			'last_updated' => date('Y-m-d H:i:s'),
			'people' => [],
		];
	}

*/
class FileDB {

	/**
	 * Read a file containing a PHP variable
	 *
	 * @param string $file File name (without extension)
	 * @return object The PHP variable (or null if the file doesn't exist)
	 */
	public function get( $file )
	{
		if ( file_exists( dirname(__FILE__) . '/' . $file . '.php' ) )
		{
			return include( dirname(__FILE__) . '/' . $file . '.php' );
		}
		else
		{
			return null;
		}
	}


	/**
	 * Save a PHP variable into a file
	 *
	 * @param string $file File name (without extension)
	 * @param object $data The PHP variable to save
	 * @return Number of bytes written (or false on error)
	 */
	public function set( $file, $data )
	{
		return file_put_contents( dirname(__FILE__) . '/' . $file . '.php', '<?php return ' . var_export( $data, true ) . ';' );
	}

}
